# Framework Imports
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status, generics, response

# Project Imports
from .serializers import FlowReadingSerializer  
from .models import FlowRating  

# View for handling flow rate data creation
class FlowReadingView(generics.CreateAPIView):  

    # Specify the serializer class
    serializer_class = FlowReadingSerializer  

    # Define the queryset for the view
    queryset = FlowRating.objects.all()  

    # Handle POST request to create a new record
    def post(self, request):  

        # Deserialize incoming data
        serializer = self.serializer_class(data=request.data)  

        # Check if the data is valid
        if serializer.is_valid():  

            # Save the valid data to the database
            serializer.save()  

            # Return the created data with HTTP 201 status
            return Response(serializer.data, status=status.HTTP_201_CREATED)  

        # Return validation errors with HTTP 400 status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
