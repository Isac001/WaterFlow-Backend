# Import Django REST framework's serializer module
from rest_framework import serializers  

# Import the FlowRating model
from .models import FlowRating  

# Serializer for FlowRating model
class FlowReadingSerializer(serializers.ModelSerializer):

    class Meta:

        # Specify the model to serialize
        model = FlowRating  
        
        # Define which fields should be serialized
        fields = ['timestamp', 'flow_rate']  