from django.db import models
from user_profile.models import Profile, User
from settings.models import Settings
from django.utils.text import slugify
from django.utils import timezone
from django.contrib import messages
import json
import datetime
# Create your models here.


SOCIAL_PROVIDERS = (
    ('facebook', 'Facebook'),
    ('github', 'Github'),
    ('google', 'Google')
)


class Social(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='social_logins'
    )
    updated_at = models.DateTimeField(auto_now=True)
    provider = models.CharField(max_length=20, choices=SOCIAL_PROVIDERS)
    social_id = models.CharField(max_length=50, unique=True)
    access_token = models.TextField()
    expires = models.IntegerField()
    scopes = models.CharField(max_length=2000, default='[]')

    @property
    def scope_list(self):
        return json.loads(self.scopes)

    @property
    def is_expired(self):
        # Returns true if expired. False otherwise
        return timezone.now() > self.updated_at + datetime.timedelta(seconds=self.expires)

    @staticmethod
    def unique_username(name, n=0):
        """Appends n to the end of the username, automatically adding 1 if exists."""
        name = slugify(name)
        if not User.objects.filter(username=name + '_' + str(n)).exists():
            return name + '_' + str(n)
        return Social.unique_username(name, n + 1)

    @staticmethod
    def unique_email(n=0):
        """Appends n to the end of the username, automatically adding 1 if exists."""
        email = f"temp_{n}@email.com"
        if not User.objects.filter(email=email).exists():
            return email
        return Social.unique_email(n + 1)

    @staticmethod
    def create_or_update(**kwargs):
        # Creates or updates a Social instance. Also creates User if email does not exist
        email = kwargs.pop('email') or Social.unique_email()
        user = kwargs.pop('user')
        request = kwargs.pop('request', None)
        first_name = kwargs.pop('first_name')
        last_name = kwargs.pop('last_name')
        social_id = kwargs['social_id']
        name = f'{first_name} {last_name}'
        user_created = False
        social_created = False

        social = Social.objects.filter(social_id=social_id)
        if social.exists():
            user = social.first().profile.user
        else:
            try:
                if user is None:
                    user = User.objects.get(email=email)
            except User.DoesNotExist:

                # Only create users if registration is open
                if not Settings.registration_is_open():
                    if request is not None:
                        messages.add_message(request, messages.INFO, 'Período de registro fechado!')
                    return None, user_created, social_created, request

                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=Social.unique_username(name),
                    email=email
                )
                user.save()
                user_created = True

                # New user created
                if Settings.default_hacker():
                    from hacker.models import Hacker
                    Hacker(profile=user.profile).save()
                if Settings.default_staff():
                    from staff.models import Staff
                    Staff(profile=user.profile).save()

        profile = user.profile
        social, social_created = Social.objects.update_or_create(
            profile=profile,
            social_id=social_id,
            provider=kwargs['provider'],
            defaults=kwargs
        )
        return social, user_created, social_created, request

    def __str__(self):
        return f"{self.provider.capitalize()} de {self.profile.user.get_full_name()} ({self.profile.user.email})"
