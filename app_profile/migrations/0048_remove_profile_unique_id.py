# Generated by Django 4.2.16 on 2025-01-19 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0047_alter_profile_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='unique_id',
        ),
    ]
