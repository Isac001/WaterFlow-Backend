from django.db import models


class MonthlyWaterConsumption(models.Model):

    date_label = models.CharField(
        max_length=255,
        verbose_name="Rótulo do Mês",
        help_text="EX: 'Janeiro de 2025'"
    )

    start_date = models.DateField(
        verbose_name="Data de Início do Mês",

    )

    end_date = models.DateField(
        verbose_name="Data do Fim do Mês"
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

        app_label = 'monthly_water_consumption'
        db_table = 'monthly_water_consumption'
        ordering = ['-start_date']