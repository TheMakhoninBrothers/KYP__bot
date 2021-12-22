import typing

from app import db
from .schemas import UserBot, UserBotFromDB


class TelegramUserRepository:

    @classmethod
    def is_exist(cls, chat_id: int) -> bool:
        return db.Session().query(
            db.Session().query(db.TelegramUser).filter_by(chat_id=chat_id).exists()).scalar()

    @classmethod
    def create(cls, user: UserBot) -> typing.Optional[UserBotFromDB]:
        if not cls.is_exist(chat_id=user.chat_id):
            new_user = db.User()
            new_user_from_bot = db.TelegramUser(chat_id=user.chat_id, username=user.username)
            new_user_from_bot.user = new_user
            db.Session().add(new_user_from_bot)
            db.Session().commit()
            return cls.read(chat_id=user.chat_id)

    @classmethod
    def read(cls, chat_id: int) -> typing.Optional[UserBotFromDB]:
        if cls.is_exist(chat_id=chat_id):
            query = db.Session().query(db.TelegramUser).filter_by(chat_id=chat_id)
            user_from_db: db.TelegramUser = query.one()
            return UserBotFromDB(id=user_from_db.id,
                                 username=user_from_db.username,
                                 chat_id=chat_id,
                                 )

    @classmethod
    def read_all(cls) -> typing.List[UserBotFromDB]:
        return [
            UserBotFromDB(id=item.id, username=item.username, chat_id=item.chat_id)
            for item in db.Session().query(db.TelegramUser).all()
        ]


__all__ = ['TelegramUserRepository']
