from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime.settings')

app = Celery('realtime')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'add-every-2-seconds': {  
        'task': 'integer.tasks.print_test',
        'schedule': 1.0,
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')