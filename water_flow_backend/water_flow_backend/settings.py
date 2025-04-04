# Import Path class to work with filesystem paths in a cross-platform way
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Django secret key (do not share in production)
SECRET_KEY = 'django-insecure-ltshk8lp_7f*my$gy-lb5+hcr1o=%!!#phi3x9$0gq5^of4r+!'

# Debug mode enabled (set to False in production)
DEBUG = True

# Allows connections from any host (restrict this in production)
ALLOWED_HOSTS = ['*']

# Installed applications for this project
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom project apps
    'apps.reader_leak',

    # Channels app for WebSocket support
    'channels',
]

# Middleware stack for handling requests/responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration for the project
ROOT_URLCONF = 'water_flow_backend.urls'

# Template engine settings (for rendering HTML if needed)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ASGI application path for WebSocket handling
ASGI_APPLICATION = 'water_flow_backend.asgi.application'

# PostgreSQL database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'waterflow', 
        'USER': 'waterflow',  
        'PASSWORD': 'root', 
        'HOST': 'localhost', 
        'PORT': '5432',
    }
}

# Password validation rules for user accounts
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Default language for the project
LANGUAGE_CODE = 'pt-br'

# Default time zone
TIME_ZONE = 'America/Fortaleza'

# Enable internationalization support
USE_I18N = True

# Enable timezone-aware datetimes
USE_TZ = True

# URL path for serving static files (CSS, JS, etc.)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Channels configuration using Redis as the backend
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)]
        }
    }
}
