# Django and Python Imports
from rest_framework.views import APIView
from rest_framework import status, generics, response
from rest_framework.permissions import IsAuthenticated

# Project Imports
from .models import BimonthlyWaterConsumption
from .serializers import *
from apps.monthly_water_consumption.models import MonthlyWaterConsumption

# Define a class-based view for listing bimonthly water consumption records
class BimonthlyWaterConsumptionView(generics.ListAPIView):
    """
    API endpoint that allows viewing bimonthly water consumption records.
    Requires authentication.
    """
    
    # Specify the permission classes required to access this view
    permission_classes = (IsAuthenticated,)
    # Define the queryset to retrieve all BimonthlyWaterConsumption objects, ordered by end_date descending
    queryset = BimonthlyWaterConsumption.objects.all().order_by('-end_date')
    # Specify the serializer class to be used for this view
    serializer_class = BimonthlyWaterConsumptionSerializer  

    # Define the handler for GET requests
    def get(self, request):
        """
        Handle GET request to list all bimonthly water consumption records.
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
        
class MonthsOnBimonthDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            # Passo 1: Busca o registro do BIMESTRE com o 'pk' da URL.
            try:
                bimester_record = BimonthlyWaterConsumption.objects.get(pk=pk)
            except BimonthlyWaterConsumption.DoesNotExist:
                return response.Response(data={"Message": "Registro de Bimestre não existe"}, status=status.HTTP_404_NOT_FOUND)
            
            # Passo 2: Busca os MESES que estão DENTRO do período do bimestre.
            # Esta consulta irá retornar uma lista de objetos MonthlyWaterConsumption.
            # Ex: [ <Mês de Maio>, <Mês de Junho> ]
            month_records = MonthlyWaterConsumption.objects.filter(
                start_date__gte=bimester_record.start_date,
                end_date__lte=bimester_record.end_date
            ).order_by('start_date')

            # Passo 3: Passa a LISTA de meses para o serializer.
            # 'many=True' é crucial aqui, pois informa ao serializer que ele
            # receberá múltiplos objetos para serializar.
            serializer = MonthsOnBimonthlySerializer(month_records, many=True)

            return response.Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(data={"ERRO": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

