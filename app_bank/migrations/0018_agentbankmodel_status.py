# Generated by Django 4.2.16 on 2025-01-29 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0017_alter_banktypemodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentbankmodel',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('hold', 'hold')], default='active', max_length=50),
        ),
    ]
