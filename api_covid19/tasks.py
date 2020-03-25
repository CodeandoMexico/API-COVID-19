
"""
========================
Celery Tasks
========================
"""

# celery imports
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import *
from .scripts.fetch_data import run

@periodic_task(run_every=(crontab(hour=2)), name="update_info: Scrap https://www.gob.mx/ website every 2 hrs")
def update_info():
    print("Updating data...")
    run()

@periodic_task(run_every=(crontab()), name="example_task: This is example task running every minute")
def example_task():
    # do some stuff
    # use models
    # make requests
    print("Running every minute...")
    run()