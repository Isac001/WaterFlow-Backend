# Import the serializers module from Django REST framework
from rest_framework import serializers
# Import the WeeklyWaterConsumption model from the current app's models
from .models import WeeklyWaterConsumption

# Define a serializer for the WeeklyWaterConsumption model
class WeeklyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = WeeklyWaterConsumption
        # Define the list of fields to include in the serialized output
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']