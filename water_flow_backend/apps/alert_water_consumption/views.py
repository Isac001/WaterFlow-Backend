# Import necessary modules and classes from Django REST framework
from rest_framework.views import APIView
from rest_framework import status, generics, response
from .serializers import AlertWaterConsumptionSerializer
from .models import AlertWaterConsumption
from rest_framework.permissions import IsAuthenticated

# Define a view class for listing AlertWaterConsumption records
class AlertWaterConsumptionView(generics.ListAPIView):
    """
    API view to retrieve a list of AlertWaterConsumption records.
    Inherits from generics.ListAPIView for standard list functionality.
    Requires authentication to access.
    """
    
    # Set permission classes - only authenticated users can access this view
    permission_classes = (IsAuthenticated,)
    
    # Define the queryset to fetch all AlertWaterConsumption records
    queryset = AlertWaterConsumption.objects.all()
    
    # Specify the serializer class for converting model instances to JSON
    serializer_class = AlertWaterConsumptionSerializer

    # Override the GET method to handle listing records
    def get(self, request):
        
        try:
            # Retrieve all AlertWaterConsumption records from the database
            alert_water_consumptions = self.get_queryset()
            
            # Serialize the data using the specified serializer
            serializer = self.serializer_class(alert_water_consumptions, many=True)
            
            # Return the serialized data with a 200 OK status
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # If an error occurs, return the error message with a 400 Bad Request status
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)