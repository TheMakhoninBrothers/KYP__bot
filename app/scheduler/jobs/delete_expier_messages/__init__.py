from datetime import timedelta

from aiogram.utils.exceptions import MessageToDeleteNotFound

from app import db
from .expire_messages_finder import ExpireMessagesFinder


async def delete_expire_message(bot, expire_message_time: timedelta):
    """Удалить все просроченные сообщения"""
    messages = ExpireMessagesFinder(expire_message_time).search()
    for message in messages:
        try:
            await bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        except MessageToDeleteNotFound:
            pass
    if messages:
        query = db.Session().query(db.UserHistory)
        query = query.filter(db.UserHistory.message_id.in_([message.message_id for message in messages]))
        if query.all():
            query.delete()


__all__ = ['delete_expire_message']
