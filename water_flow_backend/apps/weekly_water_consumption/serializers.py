# Django and Project Imports
from rest_framework import serializers

from apps.daily_water_consumption.models import DailyWaterConsumption
from .models import WeeklyWaterConsumption

# Define a serializer for the WeeklyWaterConsumption model
class WeeklyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Define class Meta
    class Meta:

        model = WeeklyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']

class DayOnWeekWaterConsumptionSerializer(serializers.ModelSerializer):

    date = serializers.DateField(source='date_of_register')
    consumption = serializers.DecimalField(source='total_consumption', max_digits=20, decimal_places=2)

    class Meta:

        model = DailyWaterConsumption
        fields = ['date', 'consumption']
