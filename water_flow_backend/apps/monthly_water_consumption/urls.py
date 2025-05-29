from django.urls import path
from .views import *

urlpatterns = [
    path('', MonthlyWaterConsumptionView.as_view(), name='monthly')
]