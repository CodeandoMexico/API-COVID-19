
"""
========================
Celery Tasks
========================
For more celery crontab info visit: 
    https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
"""

# celery imports
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import *
from .scripts.fetch_data import run

@periodic_task(run_every=(crontab(hour=2)), name="update_info: Scrap https://www.gob.mx/ website every 2 hrs")
def update_info():
    """
    This is a real world task.
    """
    print("Updating data...")
    run()

@periodic_task(run_every=(crontab()), name="example_task: This is example task running every minute")
def example_task():
    """
    This is a example task
    """
    # do some stuff
    # use models
    # make requests
    print("Running every minute...")
    run() # just for test. May be deleted later