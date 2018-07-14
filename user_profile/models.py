from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User

import re

from .tasks import send_verify_email
# Create your models here.


def gen_token():
    TOKEN_SIZE = settings.TOKEN_SIZE
    token = get_random_string(length=TOKEN_SIZE)
    if Profile.objects.filter(token=token).exists():
        return gen_token()
    return token


def gen_verification_code():
    TOKEN_SIZE = settings.TOKEN_SIZE
    verification_code = get_random_string(length=TOKEN_SIZE)
    if Profile.objects.filter(verification_code=verification_code).exists():
        return gen_verification_code()
    return verification_code


def gen_unique_id():
    TOKEN_SIZE = settings.TOKEN_SIZE
    unique_id = get_random_string(length=TOKEN_SIZE)
    if Profile.objects.filter(unique_id=unique_id).exists():
        return gen_verification_code()
    return unique_id


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Public unique ID
    unique_id = models.CharField(max_length=20, unique=True, default=gen_unique_id)

    # Log in token
    token = models.CharField(max_length=20, unique=True, default=gen_token)

    # Email verification
    verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=20, unique=True, default=gen_verification_code)

    @property
    def is_verified(self):
        """Profile's email is verified and ready to use"""
        temp_email = re.match(r'^temp_\d+@email.com$', self.user.email)
        return self.verified and temp_email is None

    @property
    def state(self):
        if self.is_hacker and self.hacker.hacker_state == 'incomplete':
            return 'incomplete'
        if not self.is_verified:
            return 'unverified'
        if self.is_hacker:
            return self.hacker.hacker_state
        return 'verified'

    # Social logins
    @property
    def has_facebook(self):
        return self.social_logins.filter(provider='facebook').exists()

    @property
    def has_github(self):
        return self.social_logins.filter(provider='github').exists()

    @property
    def has_google(self):
        return self.social_logins.filter(provider='google').exists()

    # Hacker and staff attributes
    @property
    def is_hacker(self):
        return hasattr(self, 'hacker')

    @property
    def is_staff(self):
        return hasattr(self, 'staff')

    # Methods
    def new_token(self):
        self.token = gen_token()
        self.save()
        return self.token

    def new_verification_code(self):
        self.verification_code = gen_verification_code()
        self.save()
        return self.verification_code

    def change_email(self, email):
        user = self.user
        user.email = email
        user.save()
        self.verified = False
        self.new_verification_code()
        send_verify_email.delay(self.id)

    def verify_email(self):
        self.verified = True
        self.save()
        self.new_verification_code()

    def unlink_social_provider(self, provider):
        social = self.social_logins.filter(provider=provider)
        if social.exists():
            social.first().delete()

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        profile = Profile(user=user)
        profile.save()


post_save.connect(create_profile, sender=User)
