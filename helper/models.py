from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from datetime import timedelta
from settings.models import Settings
from user_profile.models import Profile
from .subscriptions import ticket_subscription

# Create your models here.


def get_ticket_serializer(receiver):
    from .serializers import TicketSerializer
    serializer = TicketSerializer(receiver.instance)
    data = serializer.data
    return data


def get_mentor_serializer(receiver):
    from .serializers import MentorSerializer
    serializer = MentorSerializer(receiver.instance)
    data = serializer.data
    return data


class Mentor(models.Model):
    msocks_allow = True
    msocks_fields = get_mentor_serializer

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    online = models.BooleanField(default=False)
    skills = models.TextField(blank=True, default='[]')

    def set_online(self):
        self.online = True
        self.save()

    def set_offline(self):
        self.online = False
        self.save()

    @staticmethod
    def claimed_ticket_completed(sender, **kwargs):
        """A ticket that a mentor claimed was completed"""
        instance = kwargs['instance']
        if not instance.state == "completed":
            return
        self = instance.claimer.mentor
        post_save.send(Mentor, instance=self, created=False)

    def __str__(self):
        return f'Mentor {self.profile}'


def update_mentor(sender, **kwargs):
    # Updates profile
    kwargs['instance'].profile.trigger_update()


def delete_mentor(sender, **kwargs):
    profile = kwargs['instance'].profile
    profile.mentor = None
    profile.trigger_update()


post_save.connect(update_mentor, sender=Mentor)
post_delete.connect(delete_mentor, sender=Mentor)


def calc_ticket_expires():
    # Calculates the ticket expire time based on the settings
    now = timezone.now()
    settings = Settings.get()
    if settings.ticket_expire != 0:
        expires_at = now + timedelta(minutes=settings.ticket_expire)
    else:
        # if expire is disabled, expire in 1 year
        expires_at = now + timedelta(weeks=52)
    return expires_at


class Ticket(models.Model):
    msocks_allow = True
    msocks_fields = get_ticket_serializer

    creator = models.ForeignKey(
        Profile,
        related_name='tickets',
        on_delete=models.CASCADE
    )
    claimer = models.ForeignKey(
        Profile,
        related_name='claimed_tickets',
        on_delete=models.CASCADE,
        null=True
    )
    topic = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=calc_ticket_expires)
    claimed = models.DateTimeField(null=True, default=None)
    completed = models.DateTimeField(null=True, default=None)
    rating = models.IntegerField(null=True)
    comments = models.CharField(max_length=500, null=True, blank=True)

    @property
    def state(self):
        if self.completed:
            if self.rating:
                return 'completed'
            return 'unrated'
        if self.claimed:
            return 'claimed'
        if timezone.now() > self.expires:
            return 'expired'
        return 'open'


mapper = {
    'create': (ticket_subscription.CreateTicketSubscription, post_save),
    'update': (ticket_subscription.UpdateTicketSubscription, post_save),
    'delete': (ticket_subscription.DeleteTicketSubscription, post_delete)
}

for event in mapper.keys():
    # Register ticket subscriptions
    reg = mapper[event][0](mapper[event][1], event)
    reg.register(Ticket)

# Send signals when tickets are completed
post_save.connect(Mentor.claimed_ticket_completed, sender=Ticket)
