# Import Django models
from django.db import models

# Bimonthly water consumption model
class BimonthlyWaterConsumption(models.Model):

    # Bimester label field (text)
    date_label = models.CharField(
        # Max length for label
        max_length=255,
        # Display name for label
        verbose_name="Rótulo do Bimestre",
        # Help text for label
        help_text="EX: 'Janeiro de 2025'"
    # End of date_label field
    )

    # Bimester start date field
    start_date = models.DateField(
        # Display name for start date
        verbose_name="Data de Início do Bimestre",

    # End of start_date field
    )

    # Bimester end date field
    end_date = models.DateField(
        # Display name for end date
        verbose_name="Data do Fim do Bimestre"
    # End of end_date field
    )

    # Total consumption field (decimal)
    total_consumption = models.DecimalField(
        # Max digits for consumption
        max_digits=20,
        # Decimal places for consumption
        decimal_places=2,
        # Display name for consumption
        verbose_name="Consumo Total (L)",
        # Help text for consumption
        help_text="Consumo total em L/min"
    # End of total_consumption field
    )

    # String representation of the model
    def __str__(self):

        # Return formatted label and consumption
        return f"{self.date_label} - {self.total_consumption} L/min"
    
    # Meta class for model settings
    class Meta:

        # App containing this model
        app_label = 'bimonthly_water_consumption'
        # Custom database table name
        db_table = 'bimonthly_water_consumption'
        # Default ordering (newest bimester first)
        ordering = ['-start_date']