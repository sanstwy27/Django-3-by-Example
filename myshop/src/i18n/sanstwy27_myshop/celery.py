import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanstwy27_myshop.settings')

app = Celery('sanstwy27_myshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()