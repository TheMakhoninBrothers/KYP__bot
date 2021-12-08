import typing

from app import db
from .schemas import UserBot, UserBotFromDB


class TelegramUserRepository:

    @classmethod
    def is_exist(cls, user_chat_id: str) -> bool:
        return db.Session().query(
            db.Session().query(db.TelegramUser).filter_by(telegram_id=str(user_chat_id)).exists()).scalar()

    @classmethod
    def create(cls, user: UserBot) -> typing.Optional[UserBotFromDB]:
        if not cls.is_exist(user_chat_id=user.chat_id):
            new_user = db.User()
            new_user_from_bot = db.TelegramUser(telegram_id=user.chat_id,
                                                username=user.username,
                                                )
            new_user_from_bot.user = new_user
            db.Session().add(new_user_from_bot)
            db.Session().commit()
            return cls.read(user_chat_id=user.chat_id)

    @classmethod
    def read(cls, user_chat_id: str) -> typing.Optional[UserBotFromDB]:
        if cls.is_exist(user_chat_id=user_chat_id):
            query = db.Session().query(db.TelegramUser).filter_by(telegram_id=user_chat_id)
            user_from_db: db.TelegramUser = query.one()
            return UserBotFromDB(id=user_from_db.id,
                                 username=user_from_db.username,
                                 chat_id=user_chat_id,
                                 )

    @classmethod
    def read_all(cls) -> typing.List[UserBotFromDB]:
        return [UserBotFromDB(id=item.id,
                              uesrname=item.username,
                              chat_id=item.telegram_id,
                              ) for item in db.Session().query(db.TelegramUser).all()]


__all__ = ['TelegramUserRepository']
