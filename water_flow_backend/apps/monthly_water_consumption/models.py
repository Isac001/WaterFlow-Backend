# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Monthly water consumption model
class MonthlyWaterConsumption(models.Model):

    # Month label field (text)
    date_label = models.CharField(
        max_length=255,
        verbose_name=_("Rótulo do Mês"),
        help_text=_("EX: 'Janeiro de 2025'")
    )

    # Month start date field
    start_date = models.DateField(
        verbose_name=_("Data de Início do Mês")
    )

    # Month end date field
    end_date = models.DateField(
        verbose_name=_("Data de Fim do Mês")
    )

    # Total consumption field (decimal)
    total_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Consumo Total (L)"),
        help_text=_("Consumo total de água no mês em Litros")
    )

    # String representation of the model instance
    def __str__(self):
        
        # Return formatted label and total consumption
        return f"{self.date_label} - {self.total_consumption} L"
    
    # Meta class for model settings
    class Meta:
        
        app_label = 'monthly_water_consumption'
        db_table = 'monthly_water_consumption'
        ordering = ['-start_date']
        