# Django and Project Imports
from rest_framework import serializers
from .models import WeeklyWaterConsumption

# Define a serializer for the WeeklyWaterConsumption model
class WeeklyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Define class Meta
    class Meta:

        model = WeeklyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']