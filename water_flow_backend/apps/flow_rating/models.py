# Django imports
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# FlowRating model to store flow rate measurements
class FlowRating(models.Model):
    
    """
    Stores individual water flow rate measurements with timestamps.
    """

    # Timestamp for the measurement, defaulting to the current time
    times_tamp = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Horário da Medição")
    ) 
    
    # Flow rate measurement field (decimal)
    flow_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_("Taxa de Vazão"),
        help_text=_("Vazão de água medida em L/min (Litros por minuto)")
    )

    # String representation of the model instance
    def __str__(self):

        # Convert the UTC timestamp to local time for a user-friendly display
        local_time = timezone.localtime(self.times_tamp)

        # Return formatted local time and flow rate
        return f"{local_time.strftime('%d/%m/%Y %H:%M:%S')} - {self.flow_rate} L/min"

    # Meta class for model settings
    class Meta:
       
        app_label = 'flow_rating'
        db_table = 'flow_rating'
        ordering = ['-times_tamp']
        