# Generated by Django 4.2.16 on 2025-02-05 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sms', '0007_alter_smsmanagement_txn_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsmanagement',
            name='sms_from',
            field=models.CharField(default=None, help_text='SMS from `bkash` or `nagad`...', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='smsmanagement',
            name='status',
            field=models.CharField(choices=[('confirmed', 'confirmed'), ('claimed', 'claimed'), ('unclaimed', 'unclaimed')], default='unclaimed', max_length=50),
        ),
    ]
