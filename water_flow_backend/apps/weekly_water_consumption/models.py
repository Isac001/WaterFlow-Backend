# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Weekly water consumption model
class WeeklyWaterConsumption(models.Model):

    # Week label field (text)
    date_label = models.CharField(
        max_length=255, 
        verbose_name=_("Rótulo da Semana"),
        help_text=_("EX: 'Semana de 01 a 07 de Janeiro de 2025'")
    )       
   
    # Week start date field
    start_date = models.DateField(
        verbose_name=_("Data de Início da Semana")
    )

    # Week end date field
    end_date = models.DateField(
        verbose_name=_("Data de Fim da Semana")
    )

    # Total consumption field for the week (decimal)
    total_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Consumo Total (L)"),
        help_text=_("Consumo total de água na semana em Litros")
    )

    # String representation of the model instance
    def __str__(self):
        """
        Returns a string representation of the weekly consumption.
        Format: "Week Label - XXXX L"
        """
        # Return formatted label and total consumption
        return f"{self.date_label} - {self.total_consumption} L"

    # Meta class for model settings
    class Meta:
       
        app_label = 'weekly_water_consumption'
        db_table = 'weekly_water_consumption'
        ordering = ['-start_date']
      