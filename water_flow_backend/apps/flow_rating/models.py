# Import models from Django's database module
from django.db import models
# Import now and localtime from Django's timezone utilities
from django.utils.timezone import now, localtime
# Import timezone utilities from Django
from django.utils import timezone
# Import datetime from Python's standard library
from datetime import datetime

# Define a model for storing flow rate measurements
class FlowRating(models.Model):
    """
    Stores water flow rate measurements with timestamps.
    Each record represents a flow rate reading at a specific time.
    """
    
    # Define a DateTimeField for the timestamp, defaulting to the current time
    times_tamp = models.DateTimeField(default=timezone.now) 
    
    # Define a DecimalField for the flow rate measurement
    flow_rate = models.DecimalField(
        # Set the maximum number of digits allowed, including decimal places
        max_digits=6,
        # Set the number of decimal places for precision
        decimal_places=2
    )

    # Define the string representation of the model instance
    def __str__(self):
        
        # Convert the UTC timestamp to local time
        local_time = localtime(self.times_tamp)  
        # Return a formatted string with the local time and flow rate
        return local_time.strftime("%d/%m/%Y %H:%M:%S") + f" - {self.flow_rate} L/min"

    # Define metadata for the model
    class Meta:
        """
        Metadata options for the FlowRating model.
        """
        # Specify the application label for this model
        app_label = 'flow_rating'
        # Specify the custom database table name for this model
        db_table = 'flow_rating'