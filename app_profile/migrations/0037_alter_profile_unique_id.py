# Generated by Django 4.2.16 on 2025-01-16 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0036_alter_profile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unique_id',
            field=models.CharField(default='agent_990a17a69c', max_length=100, unique=True),
        ),
    ]
