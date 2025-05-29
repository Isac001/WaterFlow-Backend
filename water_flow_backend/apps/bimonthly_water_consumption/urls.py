from django.urls import path
from .views import *

urlpatterns = [
    path('', BimonthlyWaterConsumptionView.as_view(), name='bimonthly')
]