# Importing necessary Django module for URL configuration
from django.urls import path

# Importing all views from the current module
from .views import *

# Defining URL patterns for the CRUD operations
urlpatterns = [

    path("", DailyWaterConsumptionView.as_view(), name="dialy")
    
]