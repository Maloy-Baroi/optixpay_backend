# Generated by Django 4.2.16 on 2025-01-27 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settlement', '0005_settlement_commission_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settlement',
            name='amount_in_usd',
            field=models.FloatField(default=0),
        ),
    ]
