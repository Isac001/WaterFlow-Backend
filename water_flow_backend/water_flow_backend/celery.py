# Import absolute_import and unicode_literals for Python 2/3 compatibility (though less critical in modern Python)
from __future__ import absolute_import, unicode_literals
# Import the os module for interacting with the operating system, like setting environment variables
import os
# Import the Celery class for creating Celery applications
from celery import Celery
# Import crontab for defining periodic task schedules
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_flow_backend.settings')

# Initialize the Celery application with a name and specify the broker URL (Redis in this case)
app = Celery('water_flow_backend', broker='redis://redis:6379/0')

# Load Celery configuration from Django settings, using 'CELERY' as the namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task modules from a specific list of paths
# This tells Celery where to find your @shared_task decorated functions
app.autodiscover_tasks([
    # Path to the bimonthly water consumption task module
    'core.celery_tasks.bimonthly_water_consumption_task',
    # Path to the daily water consumption task module (Note: 'dialy' might be a typo for 'daily')
    'core.celery_tasks.daily_water_consumption_task', # Potential typo: dialy -> daily
    # Path to the monthly water consumption task module
    'core.celery_tasks.monthly_water_consumption_task',
    # Path to the weekly water consumption task module
    'core.celery_tasks.weekly_water_consumption_task',
    # Path to the alert water consumption task module
    'core.celery_tasks.alert_water_consumption_task',
])

# Configure worker pool restarts (can be useful for memory management in long-running workers)
app.conf.worker_pool_restarts = True
# Set the number of concurrent worker processes
app.conf.worker_concurrency = 4

# Define the schedule for periodic tasks using Celery Beat
app.conf.beat_schedule = {
    # Schedule for the daily water consumption task
    'daily_water_consumption': {
        # Name of the task to be executed
        'task': 'core.celery_tasks.daily_water_consumption_task', # Potential typo: dialy -> daily
        # Schedule to run daily at midnight (00:00)
        'schedule': crontab(hour=0, minute=0),  
    },
    
    # Schedule for the weekly water consumption task
    'weekly_water_consumption': {
        # Name of the task to be executed
        'task': 'core.celery_tasks.weekly_water_consumption_task',
        # Schedule to run every Monday at midnight (00:00)
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
    },
    
    # Schedule for the monthly water consumption task
    'monthly_water_consumption': {
        # Name of the task to be executed
        'task': 'core.celery_tasks.monthly_water_consumption_task',
        # Schedule to run on the 1st day of the month at midnight (00:00) (comment says 1:00, but code is 0:00)
        'schedule': crontab(hour=0, minute=0, day_of_month='1'),
    },
    
    # Schedule for the bimonthly water consumption task
    'bimonthly_water_consumption': {
        # Name of the task to be executed
        'task': 'core.celery_tasks.bimonthly_water_consumption_task',
        # Schedule to run on the 1st day of Jan, Mar, May, Jul, Sep, Nov at midnight (00:00) (comment says 1:00, but code is 0:00)
        'schedule': crontab(hour=0, minute=0, day_of_month='1', month_of_year='1,3,5,7,9,11'),
    },

    # Schedule for the alert water consumption task
    'alert_water_consumption': {
        # Name of the task to be executed
        'task': 'core.celery_tasks.alert_water_consumption_task',
        # Schedule to run daily at midnight (00:00)
        'schedule': crontab(hour=0, minute=0),  
    }
}