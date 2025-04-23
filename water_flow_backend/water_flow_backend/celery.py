from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Definindo settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_flow_backend.settings')

# Inicializando Celery
app = Celery('water_flow_backend')

# Carregando configs do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrindo tasks automaticamente
app.autodiscover_tasks()

# Config extra (opcional)
app.conf.worker_pool_restarts = True
app.conf.worker_concurrency = 4  # ajuste conforme sua infra

# Celery Beat: rodar cálculo semanal todo domingo às 23:59
CELERY_BEAT_SCHEDULE = {
    'weekly_water_consumption_task': {
        'task': 'apps.weekly_water_consumption.tasks.weekly_water_consumption_task',
        'schedule': crontab(hour=0, minute=0, day_of_week='sunday'),
    },
    'monthly_water_consumption_task': {
        'task': 'apps.monthly_water_consumption.tasks.monthly_water_consumption_task',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),  # Executa no 1º dia de cada mês às 01:00
    },
    'bimonthly_water_consumption_task': {
        'task': 'apps.bimonthly_water_consumption.tasks.bimonthly_water_consumption_task',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),
    },
}

