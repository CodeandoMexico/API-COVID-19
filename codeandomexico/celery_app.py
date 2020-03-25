
"""
=======================
Celery config
=======================
First steps with Django
https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
"""

from __future__ import absolute_import
from django.conf import settings
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeandomexico.settings')

app = Celery(broker=settings.CELERY_BROKER_URL, backend='rpc://', namespace='CELERY')
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(settings.INSTALLED_APPS) 

if __name__ == '__main__':
    app.start()
