from django.apps import AppConfig
from django.conf import settings
from django.core.signals import request_finished
import logging
import threading


logger = logging.getLogger(__name__)

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        if settings.configured:
           logger.info("Settings are configured in AppConfig ready function")
           from .timer import timer_to_update
           from django.dispatch import receiver
           @receiver(request_finished)
           def start_task(sender, **kwargs):
                 logger.info("Request finished signal, starting thread")
                 thread = threading.Thread(target=timer_to_update())
                 thread.start()
        else:
             logger.warning("Settings are not configured yet in ready function")