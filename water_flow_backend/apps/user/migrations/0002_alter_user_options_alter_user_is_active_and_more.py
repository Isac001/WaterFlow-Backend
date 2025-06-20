# Generated by Django 5.1.7 on 2025-06-11 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Admin status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_trusty',
            field=models.BooleanField(default=True, help_text='Designates whether this user is considered trustworthy.', verbose_name='Trusty status'),
        ),
    ]
