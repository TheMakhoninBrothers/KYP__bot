import typing

from pydantic import BaseModel


class UserBot(BaseModel):
    """Пользователь телеграмм бота"""
    chat_id: int
    username: typing.Optional[str]


class UserBotFromDB(UserBot):
    """Пользователь телеграмма из БД"""
    id: int
