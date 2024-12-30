# Generated by Django 4.2.16 on 2024-12-30 17:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0006_agentbankmodel_master_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentbankmodel',
            name='daily_limit',
            field=models.FloatField(default=0.0, help_text='Daily transaction limit', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='agentbankmodel',
            name='daily_usage',
            field=models.FloatField(default=0.0, help_text='Daily usage so far', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='agentbankmodel',
            name='maximum_amount',
            field=models.FloatField(default=25000.0, help_text='Maximum amount allowed', validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(25000.0)]),
        ),
        migrations.AlterField(
            model_name='agentbankmodel',
            name='minimum_amount',
            field=models.FloatField(default=1.0, help_text='Minimum amount allowed', validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='agentbankmodel',
            name='monthly_limit',
            field=models.FloatField(default=0.0, help_text='Monthly transaction limit', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='agentbankmodel',
            name='monthly_usage',
            field=models.FloatField(default=0.0, help_text='Monthly usage so far', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
