# Import DRF's serializers module and the model we'll serialize
from rest_framework import serializers
from .models import DailyWaterConsumption  # Note: Typo in model name ('Dialy' should be 'Daily')

# Serializer for DialyWaterConsumption model (converts model instances to JSON and vice versa)
class DailyWaterConsumptionSerializer(serializers.ModelSerializer):
    
    # Meta class defines serializer behavior and configuration
    class Meta:
        model = DailyWaterConsumption  # Specifies which model to serialize
        fields = ['id', 'date_label', 'total_consumption',  'date_of_register']