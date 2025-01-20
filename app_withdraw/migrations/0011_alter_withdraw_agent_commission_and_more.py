# Generated by Django 4.2.16 on 2025-01-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_withdraw', '0010_withdraw_cancel_callbackurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdraw',
            name='agent_commission',
            field=models.FloatField(default=5.0),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='merchant_commission',
            field=models.FloatField(default=10.0),
        ),
    ]
