# import os
# from celery import Celery
# from django.conf import settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dir')
# app = Celery('current_app_name')
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_gnk.settings')

app = Celery('desafio_gnk')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

