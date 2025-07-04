# Python and Django Imports
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register the AlertWaterConsumptionView with it
router = DefaultRouter()

# Register the AlertWaterConsumptionView with the router
router.register(r'',  AlertWaterConsumptionView, basename='alert_water_consumption')

# Define the URL patterns for the alert_water_consumption app
urlpatterns = [
    path('', include(router.urls)),
]