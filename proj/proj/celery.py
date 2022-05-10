from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from pytz import timezone
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')


app = Celery('proj')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kathmandu')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule ={
    'send-mail-every-day': {
        'task': 'reviewer.tasks.send_mail_func',
        'schedule': crontab(hour=0, minute=40),
    },
    'scrap-laptop-every-day': {
        'task': 'reviewer.tasks.LaptopScraping',
        'schedule': crontab(hour=0, minute=0),
    },
    'scrap-laptop2-every-day': {
        'task': 'reviewer.tasks.LaptopScraping2',
        'schedule': crontab(hour=0, minute=10),
    },
    'scrap-accessory-every-day': {
        'task': 'reviewer.tasks.AccessoryScraping',
        'schedule': crontab(hour=0, minute=30),
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


