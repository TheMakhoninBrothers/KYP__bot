from . import Session, User, UserFromTelegram, Record


def find_user_by__chat_id(chat_id: int):
    """Создание query UserFromTelegram по chat_id"""
    return Session().query(User).join(UserFromTelegram).filter(UserFromTelegram.chat_id == chat_id)


def find_records_by__user(user: User):
    """Создание query Record по user_module (user_id)"""
    return Session().query(Record).filter(Record.user == user)
