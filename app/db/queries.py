from . import Session, User, TelegramUser, Record


def find_telegram_user_by__chat_id(chat_id: str):
    """Создать query TelegramUser по chat_id"""
    return Session().query(TelegramUser).join(User).filter(TelegramUser.telegram_id == chat_id)


def find_records_by__user(user: User):
    """Создать query Record по user_module (user_id)"""
    return Session().query(Record).filter(Record.user == user)
