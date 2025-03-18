from django.urls import path
from .views import *

urlpatterns = [
    path('flow_reading/', FlowReadingView.as_view(), name='flow_reading')
]