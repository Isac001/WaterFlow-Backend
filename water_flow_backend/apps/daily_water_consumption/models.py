# Import models from Django's database module
from django.db import models
# Import timezone utilities from Django
from django.utils import timezone

# Define a model for tracking daily water consumption
class DailyWaterConsumption(models.Model):
    # Define a character field for a human-readable date label
    date_label = models.CharField(
        # Set the maximum length of the string
        max_length=255,
        # Set the verbose name for display in the admin interface
        verbose_name="Rótulo do Dia",
        # Provide help text for this field in forms
        help_text="EX: 'Dia 1 de Janeiro de 2025'"
    )

    # Define a date field for the registration date, defaulting to the current time
    date_of_register = models.DateField(default=timezone.now)

    # Define a decimal field for the total water consumption
    total_consumption = models.DecimalField(
        # Set the maximum number of digits allowed, including decimal places
        max_digits=20,
        # Set the number of decimal places
        decimal_places=2,
        # Set the verbose name for display in the admin interface
        verbose_name="Consumo Total (L)",
        # Provide help text for this field in forms
        help_text="Consumo total em L/min"
    )

    # Define the string representation of the model instance
    def __str__(self):
        # Return a formatted string with the date label and total consumption
        return f"{self.date_label} - {self.total_consumption} L/min"
    
    # Define metadata for the model
    class Meta:
        # Specify the application label for this model
        app_label = 'daily_water_consumption'
        # Specify the database table name for this model
        db_table = 'daily_water_consumption'