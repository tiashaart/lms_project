import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hope_academy.settings')

app = Celery('hope_academy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
