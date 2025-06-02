# Import APIView for creating custom API endpoints
from rest_framework.views import APIView
# Import status for HTTP status codes, generics for generic views, and response for API responses
from rest_framework import status, generics, response
# Import the DailyWaterConsumptionSerializer from the current app's serializers
from .serializers import DailyWaterConsumptionSerializer
# Import the DailyWaterConsumption model from the current app's models
from .models import DailyWaterConsumption  
# Import IsAuthenticated permission class to ensure user is logged in
from rest_framework.permissions import IsAuthenticated

# Define a class-based view for listing daily water consumption records
class DailyWaterConsumptionView(generics.ListAPIView):
    # Add a docstring to describe the API endpoint
    """
    API endpoint that allows viewing daily water consumption records.
    Requires authentication.
    """
    
    # Specify the permission classes required to access this view
    permission_classes = (IsAuthenticated,)
    
    # Define the queryset to retrieve all DailyWaterConsumption objects, ordered by date_of_register ascending
    queryset = DailyWaterConsumption.objects.all().order_by('-date_of_register')
    
    # Specify the serializer class to be used for this view
    serializer_class = DailyWaterConsumptionSerializer

    # Define the handler for GET requests
    def get(self, request):
        # Add a docstring to describe the GET method
        """
        Handle GET request to list all daily water consumption records.
        Returns:
            - 200 OK with serialized data on success
            - 400 Bad Request with error message on failure
        """
        # Start a try block to handle potential exceptions
        try:
            # Retrieve the queryset for this view
            queryset = self.get_queryset()

            # Paginate the queryset if pagination is configured
            page = self.paginate_queryset(queryset)

            # Check if pagination was applied
            if page is not None:

                # Serialize the paginated page data
                serializer = self.get_serializer(page, many=True)

                # Return the paginated response
                return self.get_paginated_response(serializer.data)
            
            # If not paginated, serialize the entire queryset
            serializer = self.get_serializer(queryset, many=True)
            
            # Return the serialized data with an HTTP 200 OK status
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        # Catch any exception that might occur
        except Exception as e:
            # If an error occurs, return the error message with an HTTP 400 Bad Request status
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)