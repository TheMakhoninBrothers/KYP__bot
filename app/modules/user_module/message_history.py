from aiogram import types
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from app import db
from .repository import TelegramUserRepository


class MessageHistoryController:
    """Класс для управления историей сообщений пользователя."""

    def __init__(self, message: types.Message):
        self.user = TelegramUserRepository.read(str(message.chat.id))
        self.message = message

    async def clear_history_bot(self):
        """Отчистить историю сообщений пользователя."""
        query = db.Session().query(db.UserHistory).filter(db.UserHistory.chat_id == self.user.chat_id)
        for message in query.all():
            try:
                await self.message.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
            except (MessageToDeleteNotFound, MessageCantBeDeleted):
                pass
        query.delete()
