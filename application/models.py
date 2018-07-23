from django.db import models
from hacker.models import Hacker
from django.core.validators import MinValueValidator, BaseValidator, MaxValueValidator
from django.utils import timezone
import csv
from pycpfcnpj import cpf
# Create your models here.


class CPFValidator(BaseValidator):

    code = 'cpf_value'

    def compare(self, a, b):
        return not cpf.validate(a)


def load_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        loaded_list = list(reader)
    return loaded_list


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
EXPERIENCE_LEVELS = (
    ('basic', 'Básico'),
    ('intermediate', 'Intermediário'),
    ('advanced', 'Avançado')
)
EDUCATION_CHOICES = (
    ('Ensino Fundamental', 'Ensino Fundamental'),
    ('Ensino Médio', 'Ensino Médio'),
    ('Graduação', 'Graduação'),
    ('Mestrado', 'Mestrado'),
    ('MBA', 'MBA'),
    ('Doutorado', 'Doutorado'),
    ('Pós Doutorado', 'Pós Doutorado'),
)
SCHOOL_CHOICES = load_csv('application/choices/schools.csv')
COURSE_CHOICES = load_csv('application/choices/courses.csv')
COUNTRY_CHOICES = load_csv('application/choices/country.csv')


class Application(models.Model):
    hacker = models.OneToOneField(
        Hacker,
        on_delete=models.CASCADE
    )
    # Communication
    phone = models.CharField(max_length=20, null=True, blank=False)
    # Basic
    gender = models.CharField(max_length=2, choices=GENDER_TYPES)
    age = models.IntegerField(validators=[MinValueValidator(5, "A idade mínima é 5 anos.")])
    cpf = models.CharField(max_length=20, validators=[CPFValidator(0, "CPF inválido")], default='')
    # School
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='', blank=False)
    school = models.CharField(max_length=100, null=True, blank=True, choices=SCHOOL_CHOICES)
    enroll_year = models.IntegerField(validators=[MinValueValidator(1900, "Hmm, como?"), MaxValueValidator(timezone.now().year + 1, "Hmm, como?")], null=True, blank=False)
    course = models.CharField(max_length=30, null=True, blank=True, choices=COURSE_CHOICES)
    # CV
    cv_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv = models.CharField(max_length=300, null=True, blank=True)
    cv2_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv2 = models.CharField(max_length=300, null=True, blank=True)
    # Company
    referrer = models.CharField(max_length=100, default='')
    first_timer = models.BooleanField(default=True)
    dream_company = models.CharField(max_length=100, blank=True, null=True)
    interests = models.CharField(max_length=200, default='')

    # Extra
    country = models.CharField(max_length=200, blank=True, null=True, choices=COUNTRY_CHOICES)
    state = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    can_move = models.BooleanField(default=False, blank=True)
    time_slots = models.CharField(max_length=200, blank=True, null=True)
    extra_courses = models.TextField(blank=True, null=True)
    english_level = models.CharField(max_length=20, blank=True, null=True, choices=EXPERIENCE_LEVELS)
    excel_level = models.CharField(max_length=20, blank=True, null=True, choices=EXPERIENCE_LEVELS)
    other_languages = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Aplicação de {self.hacker.profile}'
