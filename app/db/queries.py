from sqlalchemy import func

from . import Session, User, UserFromTelegram, Record, Tag


def find_user_by__chat_id(chat_id: int):
    """Создание query UserFromTelegram по chat_id"""
    return Session().query(User).join(UserFromTelegram).filter(UserFromTelegram.chat_id == chat_id)


def find_records_by__user(user: User):
    """Создание query Record по user_module (user_id)"""
    return Session().query(Record).filter(Record.user == user)


def find_records__by_tags(user, *tags):
    """Создание query Record по тегам"""
    return Session(). \
        query(Record, func.count(Record.id)). \
        join(Tag, Record.tags). \
        filter(Tag.name.in_(tags), Record.user == user). \
        group_by(Record.id). \
        having(func.count(Record.id) == len(tags))
