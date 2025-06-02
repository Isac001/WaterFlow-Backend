# Import the models module from Django's database utilities
from django.db import models

# Define a model for monthly water consumption
class MonthlyWaterConsumption(models.Model):
    # Add a docstring to describe the model's purpose
    """
    Tracks and stores monthly water consumption data.
    Each record represents water usage for a calendar month.
    """

    # Define a character field for a human-readable month label
    date_label = models.CharField(
        # Set the maximum length of the string
        max_length=255,
        # Set the verbose name for display in the admin interface
        verbose_name="Rótulo do Mês",
        # Provide help text for this field in forms
        help_text="EX: 'Janeiro de 2025'"
    )

    # Define a date field for the start date of the month
    start_date = models.DateField(
        # Set the verbose name for display in the admin interface
        verbose_name="Data de Início do Mês"
    )

    # Define a date field for the end date of the month
    end_date = models.DateField(
        # Set the verbose name for display in the admin interface
        verbose_name="Data do Fim do Mês"
    )

    # Define a decimal field for the total water consumption
    total_consumption = models.DecimalField(
        # Set the maximum number of digits allowed, including decimal places
        max_digits=20,
        # Set the number of decimal places for precision
        decimal_places=2,
        # Set the verbose name for display in the admin interface
        verbose_name="Consumo Total (L)",
        # Provide help text for this field in forms
        help_text="Consumo total em L/min"
    )

    # Define the string representation of the model instance
    def __str__(self):
        # Add a docstring to describe the string representation
        """
        String representation of monthly consumption.
        Format: "Month Year - XXXX L/min" (e.g., "Janeiro 2025 - 1250.50 L/min")
        """
        # Return a formatted string with the date label and total consumption
        return f"{self.date_label} - {self.total_consumption} L/min"
    
    # Define metadata for the model
    class Meta:
        # Add a docstring to describe the Meta class
        """
        Model metadata configuration.
        """
        # Specify the application label for this model
        app_label = 'monthly_water_consumption'
        # Specify the custom database table name for this model
        db_table = 'monthly_water_consumption'
        # Define the default ordering for querysets, newest months first
        ordering = ['-start_date']