# Generated by Django 4.2.16 on 2025-01-27 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settlement', '0004_rename_amount_after_fees_settlement_amount_after_commission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settlement',
            name='commission_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='settlement',
            name='exchange_rate',
            field=models.FloatField(default=2.5),
        ),
        migrations.AlterField(
            model_name='settlement',
            name='amount_after_commission',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='settlement',
            name='commission_percentage',
            field=models.FloatField(default=0),
        ),
    ]
