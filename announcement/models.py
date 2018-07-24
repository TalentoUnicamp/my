from django.db import models
from user_profile.models import Profile
# Create your models here.


LEVEL_CHOICES = (
    ('info', 'Informativo'),
    ('warning', 'Atenção'),
    ('error', 'Problema'),
    ('success', 'Sucesso')
)


class Announcement(models.Model):
    msocks_allow = True
    msocks_fields = [
        'id',
        ('creator_name', 'creator.full_name'),
        ('creator_unique_id', 'creator.unique_id'),
        'title',
        'created',
        'text',
        'level'
    ]

    creator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='info')
