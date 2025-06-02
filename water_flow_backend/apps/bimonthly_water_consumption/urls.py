# Import the path function from Django's URL utilities
from django.urls import path
# Import all views from the current directory's views module
from .views import *

# Define the list of URL patterns for the application
urlpatterns = [
    # Map the root URL path to the BimonthlyWaterConsumptionView class-based view
    path('', BimonthlyWaterConsumptionView.as_view(), name='bimonthly')
]