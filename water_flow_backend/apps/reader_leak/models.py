# Import Django's model framework
from django.db import models

class FlowRating(models.Model):
    
    # Stores the timestamp of the reading, auto-generated when a record is created
    timestamp = models.CharField(max_length=30)

    # Stores the flow rate value with up to 6 digits and 2 decimal places
    flow_rate = models.DecimalField(max_digits=6, decimal_places=2)

    # Returns a readable string representation of the record
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.flow_rate} L/min"
    
    class Meta:

        app_label ='reader_leak'
        db_table = 'reader_leak'
