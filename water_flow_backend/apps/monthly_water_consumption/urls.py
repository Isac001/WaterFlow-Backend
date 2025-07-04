# Django and Project Imports
from django.urls import path
from .views import *

# Define the list of URL patterns for the application
urlpatterns = [
    path('', MonthlyWaterConsumptionView.as_view(), name='monthly'),
    path('<int:pk>/', WeeksOnMonthDetail.as_view(), name='detail_week_on_month')
]