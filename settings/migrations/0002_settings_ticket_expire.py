# Generated by Django 2.0.3 on 2018-08-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='ticket_expire',
            field=models.IntegerField(default=30),
        ),
    ]
