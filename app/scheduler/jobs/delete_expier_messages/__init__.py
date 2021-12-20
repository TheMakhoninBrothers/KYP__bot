from datetime import timedelta, datetime

from app.modules.user_module.message_history_cleaner import UserHistoryCleaner


def __calculate_expire_rim(expire_delta):
    """Подсчёт даты срока хранения сообщений"""
    return datetime.now() - expire_delta


async def delete_expire_messages(bot, expire_message_time: timedelta):
    """Удаление всех просроченных сообщений"""
    expire_time = __calculate_expire_rim(expire_message_time)
    await UserHistoryCleaner(bot).clear_user_history(expire_time=expire_time)


__all__ = ['delete_expire_messages']
