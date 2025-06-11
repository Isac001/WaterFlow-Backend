# Django imports
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Project imports
from apps.daily_water_consumption.models import DailyWaterConsumption

# AlertWaterConsumption model to track water consumption alerts
class AlertWaterConsumption(models.Model):

    # Alert label to categorize the type of alert
    ALERT_TYPES = {
        ('HIGH', _('Consumo elevado')),
        ('VERY_HIGH', _('Consumo muito elevado')),
        ('EXTREME', _('Consumo excessivo')),
    }

    # Alert label
    alert_label = models.CharField(_('Label of Alert'), max_length=255)

    # Alert type
    alert_type = models.CharField(_('Type of Alert'), max_length=50, choices=ALERT_TYPES)
    
    # Date when the alert was created
    date_label_of_alert = models.DateField(
        default=now,
        verbose_name=_("Data do Alerta"),
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
        verbose_name=_("Consumo Excedido (L)"),
        help_text=_("Quantidade de consumo excedido em L/min")
    )

    # Average consumption for comparison
    average_consumption = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Média de Consumo (L)"),
        help_text=_("Média histórica de consumo em L/min")
    )
    
    # Percentage of consumption exceeded compared to the average
    percentage_exceeded = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Porcentagem Excedida (%)"),
        help_text=_("Porcentagem de consumo excedido em relação à média")
    )

    # Method to return a string representation of the alert
    def __str__(self):
        # A representação em string é executada em tempo real e geralmente 
        # não usa gettext_lazy, mas para manter a consistência com o pedido,
        # uma forma de fazer seria:
        return _('{label} - {consumo}L acima da média').format(
            label=self.alert_label,
            consumo=self.total_consumption_exceeded
        )
    
    # Meta class to define additional properties of the model
    class Meta:
        app_label = 'alert_water_consumption'
        db_table = 'alert_water_consumption'
        ordering = ['-date_label_of_alert']
        # É uma boa prática adicionar também um verbose_name para o modelo
        verbose_name = _('Alerta de Consumo de Água')
        verbose_name_plural = _('Alertas de Consumo de Água')