# Generated by Django 4.2.16 on 2025-01-14 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0029_alter_profile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unique_id',
            field=models.CharField(default='agent_ecd696d181', max_length=100, unique=True),
        ),
    ]
