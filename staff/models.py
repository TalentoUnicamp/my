from django.db import models
from django.db.models.signals import post_save, post_delete
from user_profile.models import Profile
# Create your models here.


class Staff(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Staff {self.profile}'


def update_staff(sender, **kwargs):
    # Updates profile
    kwargs['instance'].profile.trigger_update()


def delete_staff(sender, **kwargs):
    profile = kwargs['instance'].profile
    profile.staff = None
    profile.trigger_update()


post_save.connect(update_staff, sender=Staff)
post_delete.connect(delete_staff, sender=Staff)
