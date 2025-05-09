from rest_framework import serializers
from .models import DialyWaterConsumption

class DailyWaterConsumptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DialyWaterConsumption
        fields = ['__all__']
