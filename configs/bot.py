import os
from datetime import timedelta

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
hours, minutes, seconds = os.environ['MESSAGE_EXPIRE_TIME'].split('.')
MESSAGE_EXPIRE_TIME = timedelta(
    seconds=(int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds))

SEARCH_TAGS_REGEX = '#?[\w\d]+'
