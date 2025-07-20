# Imports
from rest_framework import serializers
from .models import AlertWaterConsumption

# AlertWaterConsumptionSerializer
class AlertWaterConsumptionSerializer(serializers.ModelSerializer):

    # Meta  
    class Meta:
        model = AlertWaterConsumption
        fields = ['id','alert_label', 'alert_type', 'date_label_of_alert', 'daily_water_consumption', 'total_consumption_exceeded', 'average_consumption', 'percentage_exceeded', 'is_viewed']