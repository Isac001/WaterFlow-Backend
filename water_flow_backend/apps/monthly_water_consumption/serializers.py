# Import the serializers module from Django REST framework
from rest_framework import serializers
# Import the MonthlyWaterConsumption model from the current app's models
from .models import MonthlyWaterConsumption
from apps.weekly_water_consumption.models import WeeklyWaterConsumption

# Define a serializer for the MonthlyWaterConsumption model
class MonthlyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = MonthlyWaterConsumption
        # Define the list of fields to include in the serialized output
        fields = ['id', 'date_label', 'start_date', 'end_date', 'total_consumption']


class WeeksOnTheMonthSerializer(serializers.ModelSerializer):

    consumption = serializers.DecimalField(
        source = 'total_consumption',
        max_digits=20,
        decimal_places=2
    )

    class Meta:

        model = WeeklyWaterConsumption
        fields = ['start_date', 'end_date', 'consumption']