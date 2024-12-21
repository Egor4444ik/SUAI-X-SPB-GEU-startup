import logging
from django.contrib.auth.models import User
from .models import ozon
from celery import shared_task, Celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)
app = Celery('tasks', broker='redis://127.0.0.1:6379',broker_connection_retry_on_startup=True)
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=49), do_data_update())


@shared_task()
def do_data_update():
    logger.info("do_data_update started")
    name = 'do_data_update'
    try:
        # 1. Обновление для всех пользователей
        users = User.objects.all()
        # 2. Обновление для конкретного пользователя
        #users = User.objects.filter(username='your_username') # Замените 'your_username' на нужное имя пользователя
        logger.info(users)
        for user in users:
            try:
                flag = True
                if ozon.objects.get_or_create(user=user) != False:
                    ozon_instance, created = ozon.objects.get_or_create(user=user)
                else: flag = False
                if flag:
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