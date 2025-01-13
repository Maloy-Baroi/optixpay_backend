from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0020_agentprofile_prepayment_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unique_id',
            field=models.CharField(default='agent_c7f280dcde', max_length=100, unique=True),
        ),
    ]
