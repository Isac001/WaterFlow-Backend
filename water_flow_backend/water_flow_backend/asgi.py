# Django Imports
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Project Imports
from websocket_config.consumers import FlowReadginConsumer

# Defina a variável de ambiente para as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_flow_backend.settings')

# ASGI Aplication
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/flow-reading/', FlowReadginConsumer.as_asgi()),  
        ])
    ),
})
