# Django model imports
from django.db import models

# Model for daily water consumption tracking
class DailyWaterConsumption(models.Model):
    # Human-readable date identifier (e.g., "Dia 1 de Janeiro de 2025")
    date_label = models.CharField(
        max_length=255,  # Maximum character length
        verbose_name="Rótulo do Dia",  # Admin interface label
        help_text="EX: 'Dia 1 de Janeiro de 2025'"  # Form field hint
    )

    # Water consumption measurement field
    total_consumption = models.DecimalField(
        max_digits=20,  # Total digits allowed (including decimals)
        decimal_places=2,  # Decimal precision
        verbose_name="Consumo Total (L)",  # Admin interface label
        help_text="Consumo total em L/min"  # Form field hint
    )

    # String representation for admin and debugging
    def __str__(self):
        return f"{self.date_label} - {self.total_consumption} L/min"
    
    # Model metadata configuration
    class Meta:
        app_label = 'daily_water_consumption'  # App namespace
        db_table = 'daily_water_consumption'  # Database table name
        