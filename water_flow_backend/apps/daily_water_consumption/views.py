# Import necessary modules
from rest_framework.views import APIView
from rest_framework import status, generics, response
from .serializers import DailyWaterConsumptionSerializer
from .models import DailyWaterConsumption  
from rest_framework.permissions import IsAuthenticated

# View for listing daily water consumption records
class DailyWaterConsumptionView(generics.ListAPIView):
    """
    API endpoint that allows viewing daily water consumption records.
    Requires authentication.
    """
    
    # Restrict access to authenticated users only
    permission_classes = (IsAuthenticated,)
    
    # Default queryset to retrieve all records
    queryset = DailyWaterConsumption.objects.all()
    
    # Serializer class to convert model instances to JSON
    serializer_class = DailyWaterConsumptionSerializer

    def get(self, request):
        """
        Handle GET request to list all daily water consumption records.
        Returns:
            - 200 OK with serialized data on success
            - 400 Bad Request with error message on failure
        """
        try:
            # Get all records from database
            daily_water_consumptions = self.get_queryset()
            
            # Convert queryset to JSON format
            serializer = self.serializer_class(daily_water_consumptions, many=True)
            
            # Return successful response with data
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Return error response if something goes wrong
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)