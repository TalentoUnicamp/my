from django.db import models
from user_profile.models import Profile
# Create your models here.


class Staff(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
