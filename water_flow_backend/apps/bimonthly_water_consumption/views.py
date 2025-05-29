from rest_framework.views import APIView
from rest_framework import status, generics, response
from rest_framework.permissions import IsAuthenticated
from .models import BimonthlyWaterConsumption
from .serializers import BimonthlyWaterConsumptionSerializer

class BimonthlyWaterConsumptionView(generics.ListAPIView):
    """
    API endpoint that allows viewing bimonthly water consumption records.
    Requires authentication.
    """
    
    permission_classes = (IsAuthenticated,)
    queryset = BimonthlyWaterConsumption.objects.all()
    serializer_class = BimonthlyWaterConsumptionSerializer  

    def get(self, request):
        """
        Handle GET request to list all bimonthly water consumption records.
        Returns:
            - 200 OK with serialized data on success
            - 400 Bad Request with error message on failure
        """
        try:
            bimonthly_water_consumptions = self.get_queryset()
            serializer = self.serializer_class(bimonthly_water_consumptions, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)