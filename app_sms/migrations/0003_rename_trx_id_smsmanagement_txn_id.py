# Generated by Django 4.2.16 on 2025-01-21 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_sms', '0002_alter_smsmanagement_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smsmanagement',
            old_name='trx_id',
            new_name='txn_id',
        ),
    ]
