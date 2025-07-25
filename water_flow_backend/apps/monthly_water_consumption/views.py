# Import APIView for creating custom API endpoints
from rest_framework.views import APIView
# Import status for HTTP status codes, generics for generic views, and response for API responses
from rest_framework import status, generics, response
# Import IsAuthenticated permission class to ensure user is logged in
from rest_framework.permissions import IsAuthenticated
# Import the MonthlyWaterConsumption model from the current app's models
from .models import MonthlyWaterConsumption
# Import the MonthlyWaterConsumptionSerializer from the current app's serializers
from .serializers import *

from apps.weekly_water_consumption.models import WeeklyWaterConsumption

# Define a class-based view for listing monthly water consumption records
class MonthlyWaterConsumptionView(generics.ListAPIView):
    # Add a docstring to describe the API endpoint
    """
    API endpoint that allows viewing monthly water consumption records.
    Requires authentication.
    """
    
    # Specify the permission classes required to access this view
    permission_classes = (IsAuthenticated,)
    # Define the queryset to retrieve all MonthlyWaterConsumption objects, ordered by end_date descending
    queryset = MonthlyWaterConsumption.objects.all().order_by('-end_date')
    # Specify the serializer class to be used for this view
    serializer_class = MonthlyWaterConsumptionSerializer  

    # Define the handler for GET requests
    def get(self, request):
        # Add a docstring to describe the GET method
        """
        Handle GET request to list all monthly water consumption records.
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


class WeeksOnMonthDetail(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):

        try:

            try: 

                monthly_record = MonthlyWaterConsumption.objects.get(pk=pk)

            except MonthlyWaterConsumption.DoesNotExist:

                return response.Response(
                    data={"Message": "Register of the month not found"}, status=status.HTTP_404_NOT_FOUND
                )
            
            weekly_records = WeeklyWaterConsumption.objects.filter(
                start_date__gte = monthly_record.start_date,
                end_date__lte = monthly_record.end_date
            ).order_by('start_date')

            serializer = WeeksOnTheMonthSerializer(weekly_records, many=True)

            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

             return response.Response(
                data={"ERROR": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


