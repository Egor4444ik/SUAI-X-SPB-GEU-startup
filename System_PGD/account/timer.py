import time
from .models import ozon
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)


def timer_to_update():
    logger.info('update data timer on')
    delta_hours = time.localtime().tm_hour - 23
    if delta_hours != 0:
        lost_seconds = 23*60*60 - (time.localtime().tm_sec+time.localtime().tm_min*60+time.localtime().tm_hour*60*60)
        message = 'waiting timer lost:', lost_seconds, 'seconds'
        logger.info(message)
        time.sleep(lost_seconds)
    else:
        while True:
            try:
                users = User.objects.all()
                #users = User.objects.filter(username='your_username')
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
            time.sleep(79552)