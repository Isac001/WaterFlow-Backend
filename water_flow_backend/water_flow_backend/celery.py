from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_flow_backend.settings')

# Initialize Celery application
app = Celery('water_flow_backend', broker='redis://redis:6379/0')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from core.celery_tasks
app.autodiscover_tasks([
    'core.celery_tasks.bimonthly_water_consumption_task',
    'core.celery_tasks.dialy_water_consumption_task',
    'core.celery_tasks.monthly_water_consumption_task',
    'core.celery_tasks.weekly_water_consumption_task',
    'core.celery_tasks.alert_water_consumption_task',
])

# Worker configuration
app.conf.worker_pool_restarts = True
app.conf.worker_concurrency = 4

# Beat schedule configuration
app.conf.beat_schedule = {
    # Executa diariamente à meia-noite
    'daily_water_consumption': {
        'task': 'core.celery_tasks.dialy_water_consumption_task',
        'schedule': crontab(hour=0, minute=0),  # 00:00 diariamente
        'options': {'priority': 5}
    },
    
    # Executa toda segunda-feira à meia-noite
    'weekly_water_consumption': {
        'task': 'core.celery_tasks.weekly_water_consumption_task',
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),  # Toda segunda 00:00
        'options': {'priority': 4}
    },
    
    # Executa no primeiro dia do mês às 1:00
    'monthly_water_consumption': {
        'task': 'core.celery_tasks.monthly_water_consumption_task',
        'schedule': crontab(hour=1, minute=0, day_of_month='1'),  # Dia 1 às 01:00
        'options': {'priority': 3}
    },
    
    # Executa bimestralmente nos meses ímpares às 1:00
    'bimonthly_water_consumption': {
        'task': 'core.celery_tasks.bimonthly_water_consumption_task',
        'schedule': crontab(hour=1, minute=0, day_of_month='1', month_of_year='1,3,5,7,9,11'),  # Bimestral ímpar
        'options': {'priority': 2}
    },

    # Tarefa de alerta de consumo de água
    'alert_water_consumption': {
        'task': 'core.celery_tasks.alert_water_consumption_task',
        'schedule': crontab(hour=0, minute=0),  # 00:00 diariamente
        'options': {'priority': 5}
    }
}