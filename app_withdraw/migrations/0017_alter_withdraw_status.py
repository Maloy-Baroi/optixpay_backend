# Generated by Django 4.2.16 on 2025-01-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_withdraw', '0016_withdraw_converted_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdraw',
            name='status',
            field=models.CharField(choices=[('assigned', 'assigned'), ('successful', 'successful'), ('failed', 'failed')], default='Pending', max_length=20),
        ),
    ]
