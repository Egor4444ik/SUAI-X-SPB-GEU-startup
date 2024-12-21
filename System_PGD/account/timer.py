import time
from .models import ozon
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)


def timer_to_update():
    while True:
        if time.localtime().tm_hour ==23:
            try:
                # 1. Обновление для всех пользователей
                users = User.objects.all()
                # 2. Обновление для конкретного пользователя
                # users = User.objects.filter(username='your_username') # Замените 'your_username' на нужное имя пользователя
                logger.info(users)
                for user in users:
                    try:
                        flag = True
                        if ozon.objects.get_or_create(user=user) != False:
                            ozon_instance, created = ozon.objects.get_or_create(user=user)
                        else:
                            flag = False
                        if flag:
                            ozon_instance.update_data()
                            logger.info(f"Updated data for user: {user.username}, created: {created}")
                            logger.info(f"Data: {ozon_instance.data.get('iphone_16', {})}")
                    except Exception as e:
                        logger.exception(
                            f"Error updating data for user {user.username}: {e}")  # 'exception' записывает traceback
            except Exception as e:
                logger.exception(f"Global error during data update: {e}")
            time.sleep(7200)