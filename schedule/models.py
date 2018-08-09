from django.db import models
from django.utils import timezone
from datetime import timedelta
from user_profile.models import Profile
# Create your models here.


EVENT_TYPES = (
    ('Meta', 'Meta'),
    ('Keynote', 'Keynote'),
    ('Workshop', 'Workshop'),
    ('Palestra', 'Palestra')
)


class Event(models.Model):
    msocks_allow = True
    msocks_fields = ['id', 'name', 'description']

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start = models.DateTimeField()
    duration = models.TimeField()
    require_register = models.BooleanField(default=False)
    max_attendees = models.IntegerField(null=True, blank=True)
    speaker = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="my_events"
    )
    attendees = models.ManyToManyField(
        Profile,
        related_name="selected_events"
    )
    attended = models.ManyToManyField(
        Profile,
        related_name="attended_events"
    )

    @property
    def is_full(self):
        return self.require_register and self.attendees.count() >= self.max_attendees

    @property
    def end(self):
        return self.start + timedelta(self.duration.hour, self.duration.minute)

    @property
    def is_future(self):
        now = timezone.now()
        start = self.start
        return start > now

    @property
    def is_now(self):
        start = self.start
        end = self.end
        now = timezone.now()
        return start <= now and now <= end

    @property
    def is_past(self):
        end = self.end
        now = timezone.now()
        return now > end

    def add_attendee(self, attendee):
        if self.is_full:
            return False
        self.attendees.add(attendee)
        return True

    def remove_attendee(self, attendee):
        if not self.attendee_registered(attendee):
            return False
        self.attendees.remove(attendee)
        return True

    def attendee_registered(self, attendee):
        return self.attendees.filter(pk=attendee.pk).exists()

    def checkin_attendee(self, attendee):
        if not self.attendee_registered(attendee):
            return False
        self.attended.add(attendee)
        return True

    def attendee_checkedin(self, attendee):
        return self.attended.filter(pk=attendee.pk).exists()

    def average_rating(self):
        return self.aggregate(models.Avg('feedbacks__rating'))


class Feedback(models.Model):
    attendee = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    rating = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True)
