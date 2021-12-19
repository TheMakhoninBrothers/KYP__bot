import typing

from app.modules.user_record_module.schemas import RecordFromDB


async def create_response_for__main_info(chat_id: str, username: typing.Optional[str]) -> str:
    """Создание ответа с информацией о боте"""
    return f'BOT ID: {chat_id}\n' \
           f'USERNAME: {username}\n' \
           'Доступные команды:\n' \
           '/start - Главное меню\n' \
           '/add - Добавить новую запись\n' \
           '/get - Посмотреть все свои записи\n' \
           '/get {Номер записи} - Посмотреть в отдельности\n' \
           '/del {Номер записи} - Удалить запись\n' \
           '/hide - отчистить историю сообщений\n'


async def create_response_for__records(records: typing.List[RecordFromDB]) -> str:
    """Создание ответа для списка записей"""
    return '\n\n'.join([f'Запись {record.id}\n{record.text}' for record in records])
