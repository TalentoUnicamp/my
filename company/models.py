from django.db import models
from user_profile.models import Profile
from django.db.models.signals import post_save, pre_delete
# Create your models here.


class Company(models.Model):
    msocks_allow = True
    msocks_fields = ['name', 'id', 'access_level']

    name = models.CharField(max_length=40)
    access_level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Employee(models.Model):
    msocks_allow = True
    msocks_fields = [
        ('full_name', 'profile.shortcuts.full_name'),
        ('unique_id', 'profile.unique_id'),
        ('email', 'profile.user.email'),
        ('company_name', 'company.name'),
        'checkedin'
    ]

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    checkedin = models.BooleanField(default=False)

    def check_in(self):
        self.checkedin = True
        self.save()

    def __str__(self):
        return f'{self.profile} em {self.company.name}'


class Scan(models.Model):
    """Scanned people that appear in reports"""

    msocks_allow = True
    msocks_fields = [
        'id',
        'rating',
        'comments',
        ('scannee_full_name', 'scannee.shortcuts.full_name'),
        ('scannee_unique_id', 'scannee.unique_id'),
        ('scannee_email', 'scannee.user.email'),
        ('scanner_full_name', 'scanner.shortcuts.full_name'),
        ('scanner_unique_id', 'scanner.unique_id'),
        ('scanner_email', 'scanner.user.email')
    ]

    # Person who was scanned
    scannee = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='scanned_me'
    )
    # Person who scanned
    scanner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='i_scanned'
    )
    created = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)
    comments = models.CharField(max_length=200, default='', blank=True)

    @staticmethod
    def scan_person(scannee, scanner):
        scan = Scan(
            profile=scannee,
            scanner=scanner
        )
        scan.save()

    def __str__(self):
        return f'{self.scanner.employee} escaneou {self.scannee}'


def update_employee(sender, **kwargs):
    # Updates profile
    kwargs['instance'].profile.trigger_update()


def delete_employee(sender, **kwargs):
    profile = kwargs['instance'].profile
    profile.employee = None
    profile.trigger_update()
    profile.employee = kwargs['instance']


post_save.connect(update_employee, sender=Employee)
pre_delete.connect(delete_employee, sender=Employee)
