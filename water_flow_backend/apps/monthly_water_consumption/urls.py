# Django and Project Imports
from django.urls import path
from .views import *

# Define the list of URL patterns for the application
urlpatterns = [
    path('', MonthlyWaterConsumptionView.as_view(), name='monthly')
]