# Import the os module for interacting with the operating system, like environment variables
import os

# Import the get_wsgi_application function from Django's core WSGI utilities
from django.core.wsgi import get_wsgi_application

# Set the default value for the DJANGO_SETTINGS_MODULE environment variable
# This tells Django which settings file to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_flow_backend.settings')

# Get the WSGI application callable for this Django project
application = get_wsgi_application()