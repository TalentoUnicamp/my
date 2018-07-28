from django.db.models.signals import post_save, pre_delete
from django.db import models
from django.db import IntegrityError
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
        related_name='social_logins',
        null=True
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
        user = kwargs.pop('user')
        request = kwargs.pop('request', None)
        first_name = kwargs.pop('first_name')
        last_name = kwargs.pop('last_name')
        social_id = kwargs.pop('social_id')
        name = f'{first_name} {last_name}'
        user_created = False
        social_created = False

        temp_email = False
        email = kwargs.pop('email')
        if not email or email is None:
            email = Social.unique_email()
            temp_email = True

        social = Social.objects.filter(social_id=social_id)
        if social.exists():
            user = social.first().profile.user
            # If the social email is not temporary and the user is not verified
            if not temp_email and not user.profile.is_verified:
                # update the user email and verify them
                user.email = email
                user.save()
                profile = user.profile
                profile.verified = True
                profile.save()

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
                if not temp_email:
                    profile = user.profile
                    profile.verified = True
                    profile.save()

                # New user created
                if Settings.default_hacker():
                    from hacker.models import Hacker
                    Hacker(profile=user.profile).save()
                if Settings.default_staff():
                    from staff.models import Staff
                    Staff(profile=user.profile).save()

        profile = user.profile
        try:
            social, social_created = Social.objects.update_or_create(
                profile=profile,
                social_id=social_id,
                provider=kwargs['provider'],
                defaults=kwargs
            )
        except IntegrityError:
            messages.add_message(request, messages.ERROR, f"Parece que alguém já tentou se inscrever com esse perfil do {kwargs['provider']}")
            return None, user_created, social_created, request
        return social, user_created, social_created, request

    def __str__(self):
        return f"{self.provider.capitalize()} de {self.profile}"


def update_social(sender, **kwargs):
    # Updates profile
    kwargs['instance'].profile.trigger_update()


def delete_social(sender, **kwargs):
    # Updates profile
    profile = kwargs['instance'].profile
    profile.social_logins.remove(kwargs['instance'])
    profile.trigger_update()
    profile.social_logins.add(kwargs['instance'])


post_save.connect(update_social, sender=Social)
pre_delete.connect(delete_social, sender=Social)
