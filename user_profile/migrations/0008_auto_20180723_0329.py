# Generated by Django 2.0.3 on 2018-07-23 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_shortcuts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortcuts',
            name='email',
        ),
        migrations.RemoveField(
            model_name='shortcuts',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='shortcuts',
            name='last_name',
        ),
    ]
