import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nodedoc.settings')

app = Celery('nodedoc')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# 60 second timer
app.conf.beat_schedule = {
    'scan-network-every-minute': {
        'task': 'nodes.tasks.scan_network',
        'schedule': crontab(minute='*/1'),
    },
}