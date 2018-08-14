from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.db.models import Q
from django.core.cache import cache
import datetime
import pytz
# Create your models here.


class Settings(models.Model):
    msocks_allow = True
    msocks_fields = [
        'max_hackers',
        'default_hacker',
        'default_staff',
        'auto_admit_hackers',
        'registration_opened',
        'registration_is_open',
        'can_confirm',
        'is_full',
        'hackathon_is_happening',
        'hackathon_ended',
        'registration_open_seconds',
        'registration_close_seconds',
        'confirmation_seconds',
        'hackathon_start_seconds',
        'hackathon_end_seconds',
        'ticket_expire',
        'ticket_queue_open',
        'verify_email',
    ]

    # Whether new users (created with social login) are hackers by default
    _default_hacker = models.BooleanField(default=False)
    # Whether new users (created with social login) are staff by default
    _default_staff = models.BooleanField(default=False)

    # Auto admit hackers
    auto_admit = models.BooleanField(default=False)
    # Require email verification
    verify_email = models.BooleanField(default=True)
    # Max hackers allowed
    max_hackers = models.IntegerField(default=100)

    # Hackathon timing
    # When the registration period starts
    registration_open = models.DateTimeField(default=timezone.now)
    # When it ends
    registration_close = models.DateTimeField(default=timezone.now)
    # Maximum date to confirm
    confirmation = models.DateTimeField(default=timezone.now)
    # When the event starts
    hackathon_start = models.DateTimeField(default=timezone.now)
    # When the event ends
    hackathon_end = models.DateTimeField(default=timezone.now)

    # Tickets
    ticket_expire = models.IntegerField(default=30)
    ticket_queue_open = models.BooleanField(default=False)

    @staticmethod
    def get(settings=None):
        if settings is not None:
            return settings
        cached_settings = cache.get('settings')
        if cached_settings is not None:
            return cached_settings
        settings = Settings.objects.first()
        if settings is None:
            settings = Settings()
            settings.save()
        cache.set('settings', settings)
        return settings

    # Defaults when creating new users
    @staticmethod
    def default_hacker(settings=None):
        return Settings.get(settings)._default_hacker

    @staticmethod
    def default_staff(settings=None):
        return Settings.get(settings)._default_staff

    @staticmethod
    def auto_admit_hackers(settings=None):
        return Settings.get(settings).auto_admit

    # Registration
    @staticmethod
    def registration_opened(settings=None):
        op = Settings.get(settings).registration_open
        return timezone.now() > op

    @staticmethod
    def registration_is_open(settings=None):
        settings = Settings.get(settings)
        op = settings.registration_open
        ed = settings.registration_close
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def can_confirm(extend=0, settings=None):
        # Extend parameter extends the confirmation date
        settings = Settings.get(settings)
        op = settings.registration_open
        ed = settings.confirmation
        ed += datetime.timedelta(days=extend)
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def is_full(settings=None):
        from hacker.models import Hacker
        maximum = Settings.get(settings).max_hackers
        if maximum <= 0:
            return False
        hackers = Hacker.objects.filter(Q(checked_in=True) | Q(confirmed=True) | Q(admitted=True)).distinct()
        return len(hackers) > maximum

    @staticmethod
    def hackathon_is_happening(settings=None):
        settings = Settings.get(settings)
        op = settings.hackathon_start
        ed = settings.hackathon_end
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def hackathon_ended(settings=None):
        return timezone.now() > Settings.get(settings).hackathon_end

    @staticmethod
    def registration_open_seconds(settings=None):
        return int((Settings.get(settings).registration_open - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def registration_close_seconds(settings=None):
        return int((Settings.get(settings).registration_close - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def confirmation_seconds(settings=None):
        return int((Settings.get(settings).confirmation - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_start_seconds(settings=None):
        return int((Settings.get(settings).hackathon_start - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_end_seconds(settings=None):
        return int((Settings.get(settings).hackathon_end - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    def __str__(self):
        return 'Settings'


def cache_settings(sender, **kwargs):
    settings = kwargs['instance']
    cache.set('settings', settings)


post_save.connect(cache_settings, sender=Settings)
