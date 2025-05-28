from django.db import models

class MonthlyWaterConsumption(models.Model):
    """
    Tracks and stores monthly water consumption data.
    Each record represents water usage for a calendar month.
    """

    # Human-readable month label (e.g., "Janeiro de 2025")
    date_label = models.CharField(
        max_length=255,
        verbose_name="Rótulo do Mês",  # Display name in admin interface
        help_text="EX: 'Janeiro de 2025'"  # Help text shown in forms
    )

    # First day of the month being measured
    start_date = models.DateField(
        verbose_name="Data de Início do Mês"  # Display name in admin
    )

    # Last day of the month being measured
    end_date = models.DateField(
        verbose_name="Data do Fim do Mês"  # Display name in admin
    )

    # Total water consumed during the month
    total_consumption = models.DecimalField(
        max_digits=20,  # Supports very large consumption values
        decimal_places=2,  # Tracks to 2 decimal places (0.01 L precision)
        verbose_name="Consumo Total (L)",  # Display name in admin
        help_text="Consumo total em L/min"  # Measurement units help text
    )

    def __str__(self):
        """
        String representation of monthly consumption.
        Format: "Month Year - XXXX L/min" (e.g., "Janeiro 2025 - 1250.50 L/min")
        """
        return f"{self.date_label} - {self.total_consumption} L/min"
    
    class Meta:
        """
        Model metadata configuration.
        """
        app_label = 'monthly_water_consumption'  # Associated Django app
        db_table = 'monthly_water_consumption'  # Custom database table name
        ordering = ['-start_date']  # Default sorting (newest months first)