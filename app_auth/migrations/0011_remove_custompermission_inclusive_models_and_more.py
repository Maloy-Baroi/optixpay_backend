# Generated by Django 4.2.16 on 2025-01-17 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('app_auth', '0010_remove_customgroup_group_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custompermission',
            name='inclusive_models',
        ),
        migrations.AddField(
            model_name='custompermission',
            name='inclusive_models',
            field=models.ManyToManyField(blank=True, to='contenttypes.contenttype', verbose_name='content type'),
        ),
    ]
