# Generated by Django 4.2.16 on 2025-01-13 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0025_alter_profile_unique_id'),
        ('app_deposit', '0006_alter_deposit_agent_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='agent_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_deposits', to='app_profile.agentprofile'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='merchant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_deposits', to='app_profile.merchantprofile'),
        ),
    ]
