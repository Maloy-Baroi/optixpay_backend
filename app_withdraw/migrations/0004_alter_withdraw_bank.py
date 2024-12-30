# Generated by Django 4.2.16 on 2024-12-30 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0004_agentbankmodel_remove_bankmodel_agent_and_more'),
        ('app_withdraw', '0003_withdraw_created_at_withdraw_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdraw',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_withdraw', to='app_bank.agentbankmodel'),
        ),
    ]
