# Imports
from django.urls import path
from .views import *

# Initialize the list for URL patterns
urlpatterns = [
    path('', AlertWaterConsumptionView.as_view(), name='alert_water')
]