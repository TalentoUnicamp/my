from django.db import models
from django.utils import timezone
from user_profile.models import Profile
from settings.models import Settings
from . import tasks
# Create your models here.


class Hacker(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )

    # Admitted by an admin
    admitted = models.BooleanField(default=False)
    # Declined by an admin
    declined = models.BooleanField(default=False)
    # Admitted but put on waitlist
    waitlist = models.BooleanField(default=False)
    # Datetime of waitlist (so that when the waitlist is refreshed, hackers are
    # admitted in order)
    waitlist_date = models.DateTimeField(null=True, blank=True)
    # Admitted but gave up
    withdraw = models.BooleanField(default=False)
    # Admitted and confirmed that can attend
    confirmed = models.BooleanField(default=False)
    # Checked in at the event
    checked_in = models.BooleanField(default=False)

    @property
    def hacker_state(self):
        if self.checked_in:
            return 'checkedin'
        if self.confirmed:
            return "confirmed"
        if not Settings.can_confirm(self.waitlist):
            return "late"
        if self.withdraw:
            return "withdraw"
        if self.waitlist:
            return "waitlist"
        if self.admitted:
            return "admitted"
        if self.declined:
            return "declined"
        if hasattr(self, 'application'):
            return "submitted"
        if not Settings.registration_is_open():
            return "late"
        return "incomplete"

    def admit(self, send_email=True):
        # Admit hacker and send notification email
        # Also called when a hacker that has withdrowned changes their mind
        self.admitted = True
        self.declined = False
        self.waitlist = False
        self.withdraw = False
        self.save()

        if Settings.is_full():
            # If event is full
            return self.put_on_waitlist(send_email)
        if send_email:
            tasks.send_notify_admitted.delay(self.id)

    def nag_admitted(self):
        # Remember hacker that they've been admitted
        tasks.send_nag_admitted.delay(self.id)

    def decline(self):
        self.admitted = False
        self.declined = True
        self.waitlist = False
        self.withdraw = False
        self.save()
        tasks.send_notify_decline.delay(self.id)
        # TODO: If this hacker was admitted and later
        # declined, cycle waitlist so that wailisted
        # hackers can confirm presence

    def put_on_waitlist(self, send_email=True):
        # Put hacker on waitlist (Done automatically by the server
        # if the event is full)
        self.waitlist = True
        self.waitlist_date = timezone.now()
        self.save()
        if send_email:
            tasks.send_notify_waitlist.delay(self.id)

    def unwaitlist(self):
        # Manually remove hacker from waitlist
        # This ignores the maximum number of hackers allowed
        self.waitlist = False
        self.save()
        tasks.send_notify_unwaitlist.delay(self.id)

    def withdraw_from_event(self):
        # Withdraw hacker from event
        self.confirmed = False
        self.withdraw = True
        self.admitted = False
        self.save()
        # TODO: Cycle waitlist

    def confirm(self):
        # Hacker confirmed presence
        self.confirmed = True
        self.save()
