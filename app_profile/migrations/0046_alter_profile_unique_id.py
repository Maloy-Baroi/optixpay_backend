# Generated by Django 4.2.16 on 2025-01-19 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0045_alter_profile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unique_id',
            field=models.CharField(default='agent_b20b36e407', max_length=100, unique=True),
        ),
    ]
