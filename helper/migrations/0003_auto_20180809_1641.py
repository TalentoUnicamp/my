# Generated by Django 2.0.3 on 2018-08-09 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0002_auto_20180807_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='skills',
            field=models.TextField(blank=True, default='[]'),
        ),
    ]
