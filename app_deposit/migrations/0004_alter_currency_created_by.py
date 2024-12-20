# Generated by Django 4.2.16 on 2024-12-20 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_deposit', '0003_rename_agent_deposit_agent_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
    ]