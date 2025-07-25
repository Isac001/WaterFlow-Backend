# Generated by Django 5.1.7 on 2025-06-11 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert_water_consumption', '0006_alter_alertwaterconsumption_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertwaterconsumption',
            name='alert_type',
            field=models.CharField(choices=[('HIGH', 'Consumo elevado'), ('EXTREME', 'Consumo excessivo'), ('VERY_HIGH', 'Consumo muito elevado')], max_length=50, verbose_name='Type of Alert'),
        ),
    ]
