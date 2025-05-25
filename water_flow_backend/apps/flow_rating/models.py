from django.db import models
from django.utils.timezone import now, localtime
from django.utils import timezone
from datetime import datetime

class FlowRating(models.Model):
    
    times_tamp = models.DateTimeField(default=timezone.now)
    flow_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        local_time = localtime(self.times_tamp)
        return local_time.strftime("%d/%m/%Y %H:%M:%S") + f" - {self.flow_rate} L/min"


    class Meta:
        app_label = 'flow_rating'
        db_table = 'flow_rating'
