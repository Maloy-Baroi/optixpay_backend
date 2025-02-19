# Generated by Django 4.2.16 on 2025-01-21 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_deposit', '0007_alter_deposit_agent_id_alter_deposit_merchant_id'),
        ('app_bank', '0011_agentbankmodel_deposit_commission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktypemodel',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_deposit.currency'),
        ),
        migrations.AlterField(
            model_name='banktypemodel',
            name='category',
            field=models.CharField(choices=[('p2p', 'Peer-to-Peer'), ('p2c', 'Peer-to-Customer')], default=3, help_text='Category of the bank type', max_length=3),
        ),
    ]
