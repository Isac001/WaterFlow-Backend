# Imports
from rest_framework import serializers
from .models import AlertWaterConsumption

# AlertWaterConsumptionSerializer
class AlertWaterConsumptionSerializer(serializers.ModelSerializer):

    # Meta  
    class Meta:
        model = AlertWaterConsumption
        fields = ['__all__']