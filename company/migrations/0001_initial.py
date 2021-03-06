# Generated by Django 2.0.3 on 2018-07-15 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0006_auto_20180715_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='company.Company')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('scannee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanned_me', to='user_profile.Profile')),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='i_scanned', to='user_profile.Profile')),
            ],
        ),
    ]
