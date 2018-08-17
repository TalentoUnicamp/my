from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from settings.models import Settings
from django.conf import settings
from django.contrib.auth.models import User
import re


from .tasks import send_verify_email
# Create your models here.


def gen_token():
    TOKEN_SIZE = settings.TOKEN_SIZE
    token = get_random_string(length=TOKEN_SIZE)
    return token


def gen_verification_code():
    TOKEN_SIZE = settings.TOKEN_SIZE
    verification_code = get_random_string(length=TOKEN_SIZE)
    return verification_code


def gen_unique_id():
    TOKEN_SIZE = settings.TOKEN_SIZE
    unique_id = get_random_string(length=TOKEN_SIZE)
    return unique_id


class Profile(models.Model):
    # Fields to subscribe to

    # Subscription permissions
    msocks_allow = True
    msocks_fields = [
        'unique_id',
        'full_name',
        'email',
        'state',
        'is_verified',
        'is_hacker',
        'is_staff',
        'is_admin',
        'is_employee',
        'is_mentor',
        'employee_company_access',
        'has_facebook',
        'has_github',
        'has_google'
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Public unique ID
    unique_id = models.CharField(max_length=20, unique=True, default=gen_unique_id)

    # Log in token
    token = models.CharField(max_length=20, unique=True, default=gen_token)

    # Email verification
    verified = models.BooleanField(default=False)
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

    def trigger_update(self):
        """Trigger Update
        Used to manually trigger signal updates on this model
        """
        update_shortcuts(self)
        post_save.send(Profile, instance=self, created=False)

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

    @property
    def is_admin(self):
        return self.user.is_superuser

    @property
    def is_employee(self):
        return hasattr(self, 'employee')

    @property
    def is_mentor(self):
        return hasattr(self, 'mentor')

    @property
    def employee_company_access(self):
        return (self.employee.company.access_level if self.is_employee else -1)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

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
        if Settings.get().verify_email:
            self.verified = False
            self.new_verification_code()
            send_verify_email.delay(self.id)
        else:
            self.verified = True
            self.save()

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
    user = kwargs['instance']
    if kwargs['created']:
        profile = Profile(user=user)
        profile.save()
        shortcuts = Shortcuts(profile=profile)
        shortcuts.save()
        update_shortcuts(profile)
    # Trigger profile update on user update
    else:
        if hasattr(user, 'profile'):
            user.profile.trigger_update()


post_save.connect(create_profile, sender=User)


class Shortcuts(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    # Social attributes
    has_facebook = models.BooleanField(default=False)
    has_github = models.BooleanField(default=False)
    has_google = models.BooleanField(default=False)

    # Belonging attributes
    is_hacker = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    # Control attributes
    state = models.CharField(default='', max_length=20)
    is_verified = models.BooleanField(default=False)

    full_name = models.CharField(default='', max_length=100)


def update_shortcuts(profile):
    data = {
        'has_facebook': profile.has_facebook,
        'has_github': profile.has_github,
        'has_google': profile.has_google,
        'is_hacker': profile.is_hacker,
        'is_staff': profile.is_staff,
        'is_employee': profile.is_employee,
        'is_admin': profile.is_admin,
        'is_mentor': profile.is_mentor,
        'state': profile.state,
        'is_verified': profile.is_verified,
        'full_name': profile.full_name,
    }
    Shortcuts.objects.update_or_create(
        profile=profile,
        defaults=data
    )

    def __str__(self):
        return f'Shortcut de {self.profile}'
