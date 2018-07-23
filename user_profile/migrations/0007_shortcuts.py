# Generated by Django 2.0.3 on 2018-07-23 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20180715_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcuts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_facebook', models.BooleanField(default=False)),
                ('has_github', models.BooleanField(default=False)),
                ('has_google', models.BooleanField(default=False)),
                ('is_hacker', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=200)),
                ('state', models.CharField(default='', max_length=20)),
                ('is_verified', models.BooleanField(default=False)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
        ),
    ]