# Import Django REST framework's serializer module
from rest_framework import serializers  
from django.utils.timezone import localtime
from django.utils.formats import date_format

# Import the FlowRating model
from .models import FlowRating

# Serializer for FlowRating model
class FlowReadingSerializer(serializers.ModelSerializer):

    timestamp = serializers.SerializerMethodField()
    
    # Method to convert the timestamp to a local timezone
    class Meta:

        # Specify the model to serialize
        model = FlowRating  
        
        # Define which fields should be serialized
        fields = ['timestamp', 'flow_rate'] 

    def get_timestamp(self, obj):

        return date_format(localtime(obj.timestamp), "d/m/Y H:i:s")