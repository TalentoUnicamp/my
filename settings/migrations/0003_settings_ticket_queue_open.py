# Generated by Django 2.0.3 on 2018-08-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_settings_ticket_expire'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='ticket_queue_open',
            field=models.BooleanField(default=False),
        ),
    ]