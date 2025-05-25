# Import Path class to work with filesystem paths in a cross-platform way
from pathlib import Path
from celery.schedules import crontab
import os
from dotenv import load_dotenv
import datetime


# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Import enviroment variables
load_dotenv()

# Django secret key (do not share in production)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

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
    'django_celery_beat',

    # Django REST framework for building APIs
    'rest_framework',
    'rest_framework_simplejwt',

    # Custom project apps
    'apps.flow_rating',
    'apps.weekly_water_consumption',
    'apps.monthly_water_consumption',
    'apps.bimonthly_water_consumption',
    'apps.dialy_water_consumption',
    'apps.user',

    # Channels app for WebSocket support
    'channels',

    # Core Codes
    'core',
]

AUTH_USER_MODEL = 'user.User'

# JWT token configuration settings
SIMPLE_JWT = {
    # Access token lifetime (600 minutes = 10 hours)
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=600),

    # Refresh token lifetime (24 hours)
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=24),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
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
        'NAME': os.getenv('DB_NAME'), 
        'USER': os.getenv('DB_USER'),  
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'), 
        'PORT': os.getenv('DB_PORT'),
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
            "hosts": [('redis', 6379)]
        }
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Fortaleza'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Test configuration
CELERY_TASK_ALWAYS_EAGER = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True