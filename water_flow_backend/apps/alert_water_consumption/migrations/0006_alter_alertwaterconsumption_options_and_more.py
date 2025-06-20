# Generated by Django 5.1.7 on 2025-06-11 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert_water_consumption', '0005_alter_alertwaterconsumption_alert_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alertwaterconsumption',
            options={'ordering': ['-date_label_of_alert'], 'verbose_name': 'Alerta de Consumo de Água', 'verbose_name_plural': 'Alertas de Consumo de Água'},
        ),
        migrations.AlterField(
            model_name='alertwaterconsumption',
            name='alert_label',
            field=models.CharField(max_length=255, verbose_name='Label of Alert'),
        ),
        migrations.AlterField(
            model_name='alertwaterconsumption',
            name='alert_type',
            field=models.CharField(choices=[('EXTREME', 'Consumo excessivo'), ('VERY_HIGH', 'Consumo muito elevado'), ('HIGH', 'Consumo elevado')], max_length=50, verbose_name='Type of Alert'),
        ),
    ]
