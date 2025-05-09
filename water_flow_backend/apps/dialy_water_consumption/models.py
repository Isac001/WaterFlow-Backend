from django.db import models


class DialyWaterConsumption(models.Model):

    date_label = models.CharField(
        max_length=255,
        verbose_name="Rótulo do Dia",
        help_text="EX: 'Dia 1 de Janeiro de 2025'"
    )

    total_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Consumo Total (L)",
        help_text="Consumo total em L/min"
    )

    def __str__(self):

        return f"{self.date_label} - {self.total_consumption} L/min"
    
    class Meta:

        app_label = 'dialy_water_consumption'
        db_table = 'dialy_water_consumption'
