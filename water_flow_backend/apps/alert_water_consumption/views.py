# Django and Python Imports
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Project Imports
from .serializers import AlertWaterConsumptionSerializer
from .models import AlertWaterConsumption

# Define a viewset for AlertWaterConsumption
class AlertWaterConsumptionView(viewsets.ReadOnlyModelViewSet):

    # Add a docstring to describe the API endpoint
    permission_classes = (IsAuthenticated,)
    queryset = AlertWaterConsumption.objects.all().order_by('-date_label_of_alert')
    serializer_class = AlertWaterConsumptionSerializer

    # Define the handler for GET requests
    @action(detail=False, methods=['get'])
    def unseen_count(self, request):

        count = AlertWaterConsumption.objects.filter(is_viewed=False).count()
        return Response({'count': count})
    
    # Define an action to mark all alerts as viewed
    @action(detail=False, methods=['post'])
    def mark_as_viewed(self, request):

        AlertWaterConsumption.objects.filter(is_viewed=False).update(is_viewed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)