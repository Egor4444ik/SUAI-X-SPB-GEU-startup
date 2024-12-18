from __future__ import absolute_import, unicode_literals
import logging
from logging.handlers import RotatingFileHandler
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'System_PGD.settings')

app = Celery('System_PGD')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger = logging.getLogger('celery')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('celery.log', maxBytes=10* 1024 *1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)