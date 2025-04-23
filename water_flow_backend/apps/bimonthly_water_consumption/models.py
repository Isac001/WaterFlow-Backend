from django.db import models


class BimonthlyWaterConsumption(models.Model):

    date_label = models.CharField(
        max_length=255,
        verbose_name="Rótulo do Bimestre",
        help_text="EX: 'Janeiro de 2025'"
    )

    start_date = models.DateField(
        verbose_name="Data de Início do Bimestre",

    )

    end_date = models.DateField(
        verbose_name="Data do Fim do Bimestre"
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

        app_label = 'bimonthly_water_consumption'
        db_table = 'bimonthly_water_consumption'
        ordering = ['-start_date']