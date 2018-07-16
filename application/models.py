from django.db import models
from hacker.models import Hacker
from django.core.validators import MinValueValidator
# Create your models here.


GENDER_TYPES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ('NA', 'Prefiro não dizer'),
)
SHIRT_SIZES = (
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
)
SHIRT_STYLE = (
    ('Normal', 'Normal'),
    ('Babylook', 'Babylook'),
)
CV_TYPES = (
    ('LI', 'LinkedIn'),
    ('GH', 'GitHub'),
    ('WS', 'Website'),
    ('OT', 'Outro')
)


class Application(models.Model):
    hacker = models.OneToOneField(
        Hacker,
        on_delete=models.CASCADE
    )
    # Communication
    phone = models.CharField(max_length=20, null=True, blank=True)
    # Basic
    gender = models.CharField(max_length=2, choices=GENDER_TYPES)
    age = models.IntegerField(validators=[MinValueValidator(18, "A idade mínima é 18 anos.")])
    university = models.CharField(max_length=100)
    enroll_year = models.IntegerField(null=True)
    # Needs
    diet = models.CharField(max_length=100, default="", null=True, blank=True)
    special_needs = models.CharField(max_length=100, default="", null=True, blank=True)
    # Swag
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)
    shirt_style = models.CharField(max_length=15, choices=SHIRT_STYLE)
    # CV
    cv_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv = models.CharField(max_length=300, null=True, blank=True)
    cv2_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv2 = models.CharField(max_length=300, null=True, blank=True)
    # Extra
    description = models.CharField(max_length=100, null=True)
    essay = models.TextField(null=True, blank=False)

    def __str__(self):
        return f'Aplicação de {self.hacker.profile.full_name}'
