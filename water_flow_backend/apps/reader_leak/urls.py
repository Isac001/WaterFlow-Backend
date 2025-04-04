from django.urls import path
from . import views  

urlpatterns = [
    path('flow_reading/', views.FlowReadingView.as_view(), name='flow_reading'),
]

