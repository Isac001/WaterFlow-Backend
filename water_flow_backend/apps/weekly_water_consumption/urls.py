from django.urls import path
from .views import *

urlpatterns = [
    path('', WeeklyWaterConsumptionView.as_view(), name='weekly')
]