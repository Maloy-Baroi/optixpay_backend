# Generated by Django 4.2.16 on 2024-12-17 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_profile', '0001_initial'),
        ('app_deposit', '0001_initial'),
        ('app_bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('oxp_id', models.CharField(max_length=255, unique=True)),
                ('txn_id', models.CharField(max_length=255, unique=True)),
                ('requested_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('received_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('sender_no', models.CharField(max_length=20)),
                ('receiver_no', models.CharField(max_length=20)),
                ('agent_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('merchant_commission', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Successful', 'Successful'), ('Failed', 'Failed'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired'), ('Under Review', 'Under Review'), ('On Hold', 'On Hold'), ('Declined', 'Declined')], default='Pending', max_length=20)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_withdraw', to='app_profile.profile')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_withdraw', to='app_bank.bankmodel')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currency_withdraw', to='app_deposit.currency')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_withdraw', to='app_profile.profile')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_withdraw', to='app_profile.profile')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
