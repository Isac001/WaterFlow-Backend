# Import APIView for creating API endpoints
from rest_framework.views import APIView
# Import status codes, generic views, and Response object
from rest_framework import status, generics, response
# Import the serializer for AlertWaterConsumption model
from .serializers import AlertWaterConsumptionSerializer
# Import the AlertWaterConsumption model
from .models import AlertWaterConsumption
# Import IsAuthenticated permission class for view access control
from rest_framework.permissions import IsAuthenticated

# Define a class-based view for listing water consumption alerts
class AlertWaterConsumptionView(generics.ListAPIView):
    """
    API view to retrieve a list of AlertWaterConsumption records.
    Inherits from generics.ListAPIView for standard list functionality.
    Requires authentication to access.
    """
    
    # Specify that only authenticated users can access this view
    permission_classes = (IsAuthenticated,)
    
    # Define the default queryset to retrieve all alert records
    queryset = AlertWaterConsumption.objects.all().order_by('-date_label_of_alert')
    
    # Set the serializer to be used for this view
    serializer_class = AlertWaterConsumptionSerializer

    # Define the method to handle GET requests
    def get(self, request):
        
        # Start a try block for error handling
        try:
            # Retrieve the queryset for the view
            queryset = self.get_queryset()

            # Paginate the queryset if pagination is configured
            page = self.paginate_queryset(queryset)

            # Check if pagination returned a page object
            if page is not None:

                # Serialize the current page of data
                serializer = self.get_serializer(page, many=True)

                # Return the paginated response
                return self.get_paginated_response(serializer.data)
            
            # If not paginated, serialize the entire queryset
            serializer = self.get_serializer(queryset, many=True)
            
            # Return the serialized data with an HTTP 200 OK status
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        # Catch any exception that occurs during the process
        except Exception as e:
            # Return an error response with the exception message and HTTP 400 status
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)