# Django Imports
from django.urls import re_path

# Project Imports
from . import consumers

# WebSocket Paths
websocket_urlpatterns = [
    re_path(r'ws/flow-reading/', consumers.FlowReadginConsumer)
]
