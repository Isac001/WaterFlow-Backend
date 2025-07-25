# Django and Python Imports
from rest_framework.views import APIView
from rest_framework import status, generics, response
from rest_framework.permissions import IsAuthenticated

# Project Imports
from .serializers import DailyWaterConsumptionSerializer
from .models import DailyWaterConsumption  

# Define a class-based view for listing daily water consumption records
class DailyWaterConsumptionListView(generics.ListAPIView):

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
        

class DailyWaterConsumptionDetailView(generics.RetrieveAPIView):

    # Specify the permission classes required to access this view
    permission_classes = (IsAuthenticated,)
    
    # Define the queryset to retrieve all DailyWaterConsumption objects, ordered by date_of_register ascending
    queryset = DailyWaterConsumption.objects.all().order_by('-date_of_register')
    
    # Specify the serializer class to be used for this view
    serializer_class = DailyWaterConsumptionSerializer

    def get(self, request, pk):

        daily_water_consumption = self.get_queryset(pk=pk)


        serializer = self.serializer_class(daily_water_consumption)

        try:

            if serializer.is_valid():
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
