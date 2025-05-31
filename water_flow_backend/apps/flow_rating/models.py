# Django imports
from django.db import models
from django.utils.timezone import now, localtime
from django.utils import timezone
from datetime import datetime

class FlowRating(models.Model):
    """
    Stores water flow rate measurements with timestamps.
    Each record represents a flow rate reading at a specific time.
    """
    
    # Timestamp of when the measurement was taken (auto-set to current time if not specified)
    times_tamp = models.DateTimeField(default=timezone.now)  # Note: Field name has typo ('times_tamp' should be 'timestamp')
    
    # Flow rate measurement in liters per minute (L/min)
    flow_rate = models.DecimalField(
        max_digits=6,      # Maximum of 6 digits total (including decimal places)
        decimal_places=2    # Store with 2 decimal places precision
    )

    # Returns a string representation of the FlowRating object
    def __str__(self):
        
        local_time = localtime(self.times_tamp)  # Convert to local timezone
        return local_time.strftime("%d/%m/%Y %H:%M:%S") + f" - {self.flow_rate} L/min"

    class Meta:
        """
        Metadata options for the FlowRating model.
        """
        app_label = 'flow_rating'    # Specifies which app owns this model
        db_table = 'flow_rating'    # Custom database table name