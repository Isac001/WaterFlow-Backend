# Imports
from django.urls import path
from .views import *

# Initialize the list for URL patterns
urlpatterns = [
    # Map the root URL ('') to AlertWaterConsumptionView, name it 'alert_water'
    path('', AlertWaterConsumptionView.as_view(), name='alert_water')
]