# Generated by Django 4.2.16 on 2024-12-30 03:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0003_alter_banktypemodel_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentBankModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('bank_unique_id', models.CharField(help_text='Unique identifier for the bank', max_length=100, unique=True)),
                ('bank_name', models.CharField(help_text='Name of the bank', max_length=100)),
                ('account_number', models.CharField(help_text='Account number in the format +880XXXXXXXXX', max_length=15, validators=[django.core.validators.RegexValidator('^\\+880\\d{9,10}$', message='Account number must start with +880 and contain 9-10 digits')])),
                ('minimum_amount', models.DecimalField(decimal_places=2, default=1.0, help_text='Minimum amount allowed', max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('maximum_amount', models.DecimalField(decimal_places=2, default=25000.0, help_text='Maximum amount allowed', max_digits=10, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(25000.0)])),
                ('daily_limit', models.DecimalField(decimal_places=2, default=0.0, help_text='Daily transaction limit', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('daily_usage', models.DecimalField(decimal_places=2, default=0.0, help_text='Daily usage so far', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('monthly_limit', models.DecimalField(decimal_places=2, default=0.0, help_text='Monthly transaction limit', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('monthly_usage', models.DecimalField(decimal_places=2, default=0.0, help_text='Monthly usage so far', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('app_key', models.CharField(help_text='API key for the application', max_length=255)),
                ('secret_key', models.CharField(help_text='Secret key for the application', max_length=255)),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
                'db_table': 'agent_bank',
            },
        ),
        migrations.RemoveField(
            model_name='bankmodel',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='bankmodel',
            name='bank_type',
        ),
        migrations.RemoveField(
            model_name='bankmodel',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bankmodel',
            name='updated_by',
        ),
    ]
