from rest_framework.views import APIView
from rest_framework import status, generics, response
from .serializers import DailyWaterConsumptionSerializer
from .models import DialyWaterConsumption
from rest_framework.permissions import IsAuthenticated

class DailyWaterConsumptionView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = DialyWaterConsumption.objects.all()
    serializer_class = DailyWaterConsumptionSerializer

    def get(self, request):

        try:
            
            daily_water_consumptions = self.get_queryset()
            serializer = self.serializer_class(daily_water_consumptions, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)    