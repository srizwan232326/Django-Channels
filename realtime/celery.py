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
        'schedule': 100.0,
    },

    'Plctest': {
        'task': 'integer.tasks.mplc_main_task',
        'schedule': 10.0,
        'args': ('192.169.4.30', 8001, 'L', 'binary'),
    },
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')