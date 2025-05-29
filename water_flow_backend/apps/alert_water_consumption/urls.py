from django.urls import path
from .views import *

urlpatterns = [
    path('', AlertWaterConsumptionView.as_view(), name='alert_water')
]