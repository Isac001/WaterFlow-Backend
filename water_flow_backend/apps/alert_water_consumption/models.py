# Django imports
from django.db import models
from django.utils.timezone import now

# Project imports
from apps.daily_water_consumption.models import DailyWaterConsumption

# AlertWaterConsumption model to track water consumption alerts
class AlertWaterConsumption(models.Model):

    # Alert label to categorize the type of alert
    ALERT_TYPES = {
        ('HIGH', 'Consumo elevado'),
        ('VERY_HIGH', 'Consumo muito elevado'),
        ('EXTREME', 'Consumo excessivo'),
    }

    # Alert label
    alert_label = models.CharField(
        max_length=255
        )

    # Alert type
    alert_type = models.CharField(
        max_length=50,
        choices=ALERT_TYPES
    )
    # Date when the alert was created
    date_label_of_alert = models.DateField(
        default=now,
        verbose_name="Data do Alerta",
    )

    # Foreign key to the DialyWaterConsumption model
    daily_water_consumption = models.ForeignKey(
        DailyWaterConsumption,
        on_delete=models.CASCADE, 
        related_name='alerts'
        )

    # Fields to store water consumption data
    total_consumption_exceeded = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Consumo Excedido (L)",
        help_text="Quantidade de consumo excedido em L/min"
    )

    # Average consumption for comparison
    average_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Média de Consumo (L)",
        help_text="Média histórica de consumo em L/min"
    )
    
    # Percentage of consumption exceeded compared to the average
    percentage_exceeded = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Porcentagem Excedida (%)",
        help_text="Porcentagem de consumo excedido em relação à média"
    )

    # Method to return a string representation of the alert
    def __str__(self):
        return f"{self.alert_label} - {self.total_consumption_exceeded}L acima da média"
    
    # Meta class to define additional properties of the model
    class Meta:

        app_label = 'alert_water_consumption'
        db_table = 'alert_water_consumption'
        ordering = ['-date_label_of_alert']