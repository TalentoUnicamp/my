# Generated by Django 2.0.3 on 2018-07-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20180717_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='access_level',
            field=models.IntegerField(default=0),
        ),
    ]
