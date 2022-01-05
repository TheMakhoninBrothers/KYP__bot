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
           '/hide - очистить историю сообщений\n'


async def create_response_for__records(records: typing.List[RecordFromDB]) -> str:
    """Создание ответа для списка записей"""
    if records:
        text = [await create_response_for__record(record) for record in records]
        return '\n\n'.join(text)
    return 'У вас нет записей'


async def create_response_for__record(record: RecordFromDB) -> str:
    """Создание ответа для записи"""
    return f'<b>Запись</b> {record.id}\n' \
           f'<b>Теги:</b> {" ".join([f"#{tag}" for tag in record.tags])}\n' \
           f'{record.text}'


async def create_response_for__search_by_tags(records: typing.List[RecordFromDB], tags: typing.List[str]) -> str:
    """Создание ответа для поиска по тегам"""
    head_text = f'🔍 <b>Поиск по тегам:</b> #{" #".join(tags)}\n'
    if records:
        return f'{head_text}\n' \
               f'{await create_response_for__records(records)}'
    return f'{head_text}\n' \
           f'<i>Записи не найдены</i>'
