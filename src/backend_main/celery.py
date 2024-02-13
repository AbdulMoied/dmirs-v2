import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')

app = Celery('backend_main', backend='redis://redis:6379', broker='redis://redis:6379')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.autodiscover_tasks(settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
