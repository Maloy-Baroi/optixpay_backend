# Generated by Django 4.2.16 on 2025-01-17 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0038_alter_profile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unique_id',
            field=models.CharField(default='agent_405e070ecc', max_length=100, unique=True),
        ),
    ]
