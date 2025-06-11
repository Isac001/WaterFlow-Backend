# Import Django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Daily water consumption model
class DailyWaterConsumption(models.Model):
    
    # Day label field (text)
    date_label = models.CharField(
        max_length=255,
        verbose_name=_("Rótulo do Dia"),
        help_text=_("EX: '01 de Janeiro de 2025'")
    )

    # Registration date field, defaults to the current date
    date_of_register = models.DateField(
        default=timezone.now,
        verbose_name=_("Data do Registro")
    )

    # Total consumption field (decimal)
    total_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Consumo Total (L)"),
        help_text=_("Consumo total de água no dia em Litros")
    )

    # String representation of the model
    def __str__(self):
        # Return formatted label and consumption
        return f"{self.date_label} - {self.total_consumption} L"
    
    # Meta class for model settings
    class Meta:
        
        app_label = 'daily_water_consumption'
        db_table = 'daily_water_consumption'
        ordering = ['-date_of_register']
        