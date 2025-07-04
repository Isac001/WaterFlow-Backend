# Django and Python Imports
from rest_framework.views import APIView
from rest_framework import status, generics, response
from rest_framework.permissions import IsAuthenticated

# Project Imports
from .models import WeeklyWaterConsumption
from .serializers import *

# Define a class-based view for listing weekly water consumption records
class WeeklyWaterConsumptionView(generics.ListAPIView):
    """
    API endpoint that allows viewing weekly water consumption records.
    Requires authentication.
    """
    
    # Specify the permission classes required to access this view
    permission_classes = (IsAuthenticated,)

    # Define the queryset to retrieve all WeeklyWaterConsumption objects, ordered by end_date descending
    queryset = WeeklyWaterConsumption.objects.all().order_by('-end_date')

    # Specify the serializer class to be used for this view
    serializer_class = WeeklyWaterConsumptionSerializer  

    # Define the handler for GET requests
    def get(self, request):

        """
        Handle GET request to list all weekly water consumption records.
        Returns:
            - 200 OK with serialized data on success
            - 400 Bad Request with error message on failure
        """

        # Start a try block to handle potential exceptions
        try:

            # Retrieve the queryset for this view (Note: comment refers to AlertWaterConsumption, but context is Weekly)
            queryset = self.get_queryset()

            # Paginate the queryset if pagination is configured
            page = self.paginate_queryset(queryset)

            # Check if pagination was applied and a page object was returned
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
   
# Detail the days on week register
class DaysOfWeekDetail(generics.RetrieveAPIView):

    # Necessary user to be authenticated
    permission_classes = (IsAuthenticated,)


    # Detail Function
    def get(self, request, pk):

        try:

            try:

                weekly_record = WeeklyWaterConsumption.objects.get(pk=pk)

            except WeeklyWaterConsumption.DoesNotExist:


                return response.Response(data={"message": "Weekly record not found or does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            daily_records = DailyWaterConsumption.objects.filter(
                date_of_register__range=(weekly_record.start_date, weekly_record.end_date)
            ).order_by('date_of_register')

            serializer = DayOnWeekWaterConsumptionSerializer(daily_records, many=True)

            return response.Response(data=serializer.data, status=status.HTTP_200_OK)


        except Exception as e:

            return response.Response(data={"ERROR": f'{str(e)}'}, status=status.HTTP_404_NOT_FOUND)

