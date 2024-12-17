# Generated by Django 4.2.16 on 2024-12-12 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_deposit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('currency_code', models.CharField(max_length=255, unique=True)),
                ('currency_symbol', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='received_currency',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='requested_currency',
        ),
        migrations.AddField(
            model_name='deposit',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currency_deposits', to='app_deposit.currency'),
        ),
    ]
