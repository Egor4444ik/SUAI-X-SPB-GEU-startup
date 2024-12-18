import logging
from django.contrib.auth.models import User
from .models import ozon
from celery import shared_task, Celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)
app = Celery()
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

@app.task
def do_data_update(sender, **kwards):
    logger.info("do_data_update started")
    try:
        # 1. Обновление для всех пользователей
        users = User.objects.all()
        # 2. Обновление для конкретного пользователя
        #users = User.objects.filter(username='your_username') # Замените 'your_username' на нужное имя пользователя

        for user in users:
            try:
                ozon_instance, created = ozon.objects.get_or_create(user=user)
                ozon_instance.update_data()
                logger.info(f"Updated data for user: {user.username}, created: {created}")
                logger.info(f"Data: {ozon_instance.data.get('iphone_16', {})}")
            except Exception as e:
                logger.exception(f"Error updating data for user {user.username}: {e}") #  'exception' записывает traceback
    except Exception as e:
        logger.exception(f"Global error during data update: {e}")

@app.task
def test(arg):
    print(arg)