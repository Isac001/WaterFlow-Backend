# Import models from Django's database module
from django.db import models

# Define a model for tracking weekly water consumption
class WeeklyWaterConsumption(models.Model):

    # Define a character field for a human-readable week label
    date_label = models.CharField(
        # Set the maximum length of the string
        max_length=255, 
        # Set the verbose name for display in the admin interface
        verbose_name="Rótulo da Semana",
        # Provide help text for this field in forms
        help_text="EX: 'Semana 01 - 07 de Janeiro de 2025'"
    )       
   
    # Define a date field for the start date of the week
    start_date = models.DateField(
        # Set the verbose name for display in the admin interface
        verbose_name="Data de Início"
    )

    # Define a date field for the end date of the week
    end_date = models.DateField(
        # Set the verbose name for display in the admin interface
        verbose_name="Data de Fim"
    )

    # Define a decimal field for the total water consumption during the week
    total_consumption = models.DecimalField(
        # Set the maximum number of digits allowed, including decimal places
        max_digits=20,
        # Set the number of decimal places for precision
        decimal_places=2,
        # Set the verbose name for display in the admin interface
        verbose_name="Consumo Total (L)",
        # Provide help text for this field in forms
        help_text="Consumo total em L/min")

    # Define the string representation of the model instance
    def __str__(self):
        
        
        # Return a formatted string with the date label and total consumption
        return f"{self.date_label} - {self.total_consumption} L/min"

    # Define metadata for the model
    class Meta:

        # Specify the application label for this model
        app_label = 'weekly_water_consumption'
        # Specify the custom database table name for this model
        db_table = 'weekly_water_consumption'
        # Define the default ordering for querysets, newest weeks first by start date
        ordering = ['-start_date']