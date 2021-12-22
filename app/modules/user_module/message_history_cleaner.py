import typing
from datetime import datetime

from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from app import db


class UserHistoryCleaner:
    """Очистка истории сообщений пользователей"""

    def __init__(self, bot):
        self.bot = bot

    async def clear_user_history(
            self,
            chat_id: typing.Optional[str] = None,
            expire_time: typing.Optional[datetime] = None,
    ):
        """Удаление сообщений в приватной беседе пользователей"""
        query = db.Session().query(db.UserPrivateMessage).join(db.UserFromTelegram)
        if chat_id:
            query = query.filter(db.UserFromTelegram.chat_id == chat_id)
        if expire_time:
            query = query.filter(db.UserPrivateMessage.created_at < expire_time)
        await self._delete_messages(query.all())

    async def _delete_messages(self, messages: typing.List[db.UserPrivateMessage]):
        """
        Удаление сообщений в:
         - истории сообщений в боте
         - хранилище (БД)
        """
        for message in messages:
            try:
                await self.bot.delete_message(chat_id=message.user.chat_id, message_id=message.message_id)
            except (MessageToDeleteNotFound, MessageCantBeDeleted):
                pass
            finally:
                db.Session().delete(message)
        db.Session().commit()
