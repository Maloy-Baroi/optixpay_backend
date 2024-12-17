# Generated by Django 4.2.16 on 2024-12-17 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_deposit', '0002_alter_currency_options_alter_currency_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposit',
            old_name='agent',
            new_name='agent_id',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='customer',
            new_name='customer_id',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='merchant',
            new_name='merchant_id',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='receiver_no',
            new_name='receiver_account',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='sender_no',
            new_name='sender_account',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='received_amount',
            new_name='sent_amount',
        ),
        migrations.RenameField(
            model_name='deposit',
            old_name='received_currency',
            new_name='sent_currency',
        ),
    ]
