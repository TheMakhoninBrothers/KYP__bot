from . import Session, User, TelegramUser, Record


def find_user_by__chat_id(chat_id: int):
    """Создание query TelegramUser по chat_id"""
    return Session().query(User).join(TelegramUser).filter(TelegramUser.chat_id == chat_id)


def find_records_by__user(user: User):
    """Создание query Record по user_module (user_id)"""
    return Session().query(Record).filter(Record.user == user)
