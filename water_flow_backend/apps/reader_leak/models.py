# Import Django's model framework
from django.db import models
from django.utils.timezone import now
from django.utils.timezone import now, localtime
from django.utils.formats import date_format

class FlowRating(models.Model):
    
    # Stores the timestamp of the reading, auto-generated when a record is created
    times_tamp = models.DateTimeField(default=now)

    # Stores the flow rate value with up to 6 digits and 2 decimal places
    flow_rate = models.DecimalField(max_digits=6, decimal_places=2)

    # Returns a readable string representation of the record
    def __str__(self):
        
        local_time = localtime(self.times_tamp)
        return date_format(local_time, "d/m/Y H:i:s") + f" - {self.flow_rate} L/min"
    
    # Meta class to define additional properties for the model
    class Meta:

        app_label ='reader_leak'
        db_table = 'reader_leak'
