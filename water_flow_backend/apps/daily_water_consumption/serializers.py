# Django and Project Imports
from rest_framework import serializers
from .models import DailyWaterConsumption 

# Serializer for DialyWaterConsumption model 
class DailyWaterConsumptionSerializer(serializers.ModelSerializer):
    
    # Meta class 
    class Meta:
        model = DailyWaterConsumption  
        fields = ['id', 'date_label', 'total_consumption',  'date_of_register']