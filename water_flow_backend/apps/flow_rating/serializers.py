# Django and Python Imports
from rest_framework import serializers  
from django.utils.timezone import localtime
from django.utils.formats import date_format

# Project Imports
from .models import FlowRating

# Define a serializer class for the FlowRating model
class FlowReadingSerializer(serializers.ModelSerializer):

    # Define a custom field for the times_tamp that uses a method
    times_tamp = serializers.SerializerMethodField()
    
    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = FlowRating  
        
        # Define the list of fields to include in the serialized output
        fields = ['times_tamp', 'flow_rate'] 

    # Define a method to get the formatted value for the times_tamp field
    def get_times_tamp(self, obj):

        # Convert the timestamp to local time and format it as "d/m/Y H:i:s"
        return date_format(localtime(obj.times_tamp), "d/m/Y H:i:s")