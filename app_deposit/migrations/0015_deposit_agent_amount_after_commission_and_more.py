# Generated by Django 4.2.16 on 2025-02-01 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_deposit', '0014_alter_deposit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='agent_amount_after_commission',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='deposit',
            name='agent_balance_should_be',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='deposit',
            name='merchant_amount_after_commission',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='deposit',
            name='merchant_balance_should_be',
            field=models.FloatField(default=0),
        ),
    ]
