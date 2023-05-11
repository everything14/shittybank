import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shittybank.settings')

app = Celery('shittybank')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
