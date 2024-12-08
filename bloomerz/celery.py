from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloomerz.settings')

app = Celery('bloomerz')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'increment_days': {
        'task': 'main_app.tasks.increment_days_for_water',
        'schedule': crontab(minute=0, hour=0),
    },
}