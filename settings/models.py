from django.db import models
from django.utils import timezone
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
    ]

    # Whether new users (created with social login) are hackers by default
    _default_hacker = models.BooleanField(default=False)
    # Whether new users (created with social login) are staff by default
    _default_staff = models.BooleanField(default=False)

    # Auto admit hackers
    auto_admit = models.BooleanField(default=False)
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

    @staticmethod
    def get():

        settings = Settings.objects.first()
        if settings is None:
            settings = Settings()
            settings.save()
        return settings

    # Defaults when creating new users
    @staticmethod
    def default_hacker():
        return Settings.get()._default_hacker

    @staticmethod
    def default_staff():
        return Settings.get()._default_staff

    @staticmethod
    def auto_admit_hackers():
        return Settings.get().auto_admit

    # Registration
    @staticmethod
    def registration_opened():
        op = Settings.get().registration_open
        return timezone.now() > op

    @staticmethod
    def registration_is_open():
        op = Settings.get().registration_open
        ed = Settings.get().registration_close
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def can_confirm(extend=0):
        # Extend parameter extends the confirmation date
        op = Settings.get().registration_open
        ed = Settings.get().confirmation
        ed += datetime.timedelta(days=extend)
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def is_full():
        from hacker.models import Hacker
        maximum = Settings.get().max_hackers
        if maximum <= 0:
            return False
        hackers = [None for hacker in Hacker.objects.all() if hacker.profile.state in ['admitted', 'confirmed', 'checked_in']]
        return len(hackers) > maximum

    @staticmethod
    def hackathon_is_happening():
        op = Settings.get().hackathon_start
        ed = Settings.get().hackathon_end
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def hackathon_ended():
        return timezone.now() > Settings.get().hackathon_end

    @staticmethod
    def registration_open_seconds():
        return int((Settings.get().registration_open - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def registration_close_seconds():
        return int((Settings.get().registration_close - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def confirmation_seconds():
        return int((Settings.get().confirmation - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_start_seconds():
        return int((Settings.get().hackathon_start - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_end_seconds():
        return int((Settings.get().hackathon_end - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    def __str__(self):
        return 'Settings'
