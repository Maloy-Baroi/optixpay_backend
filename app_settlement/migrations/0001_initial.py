# Generated by Django 4.2.16 on 2025-01-21 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_profile', '0052_merchantwallet_deposit_commission_and_more'),
        ('app_deposit', '0007_alter_deposit_agent_id_alter_deposit_merchant_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('settlement_id', models.CharField(max_length=20, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commission_percentage', models.FloatField()),
                ('amount_after_fees', models.FloatField()),
                ('txn_id', models.CharField(max_length=20, unique=True)),
                ('usdt_address', models.CharField(max_length=34)),
                ('status', models.CharField(choices=[('complete', 'Complete'), ('pending', 'Pending'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_deposit.currency')),
                ('merchant_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_profile.merchantprofile')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]
