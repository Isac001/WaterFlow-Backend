# Generated by Django 5.1.7 on 2025-04-22 19:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader_leak', '0002_alter_flowrating_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowrating',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
