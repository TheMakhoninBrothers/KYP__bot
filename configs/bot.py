import os
from datetime import timedelta

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
expire_time = os.environ['MESSAGE_EXPIRE_TIME'].split('.')
MESSAGE_EXPIRE_TIME = timedelta(
    seconds=(int(expire_time[0]) * 60 * 60) + (int(expire_time[1]) * 60) + int(expire_time[2]))
