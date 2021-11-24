from aiogram import Bot, Dispatcher, types

from app import resourses as modules
from configs import bot as bot_settings

bot = Bot(token=bot_settings.TOKEN)

dp = Dispatcher(bot)


def auto_registration(func):
    async def wrapper(message: types.Message):
        if modules.user.TelegramUserRepository.is_exist(str(message.chat.id)):
            user = modules.user.TelegramUserRepository.read(str(message.chat.id))
        else:
            user = modules.user.schemas.UserBot(username=message.chat.username,
                                                chat_id=message.chat.id,
                                                )
            user = modules.user.TelegramUserRepository.create(user)
        return await func(message, user)

    return wrapper


@dp.message_handler(commands='start')
@auto_registration
async def main_menu(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    await message.reply(f'BOT ID: {user.chat_id}\n'
                        f'USERNAME: {user.username}\n'
                        'Доступные команды:\n'
                        '/start - Главное меню\n'
                        '/add - Добавить новую запись\n'
                        '/get - Посмотреть все свои записи\n'
                        '/get <Номер записи> - Посмотреть в отдельности'
                        '/del <Номер записи> - Удалить запись'
                        )


@dp.message_handler(commands='add')
@auto_registration
async def add_record(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    new_text = message.text[len('/add'):].strip()
    if new_text:
        record = modules.record.schemas.Record(text=new_text,
                                               chat_id=user.chat_id)
        new_record = modules.record.RecordRepository.create(record)
        if new_record:
            await message.reply(f'Запись успешно сохранена под номером: {new_record.id}')
    else:
        await message.reply('Вам нужно добавить текст после /add\n'
                            'Например: "/add Моя новая запись"')


@dp.message_handler(commands='get')
@auto_registration
async def get_records(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    record_id = message.text[len('/get'):].strip()
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None
    if record_id:
        record = modules.record.RecordRepository.read(int(record_id))
        await message.reply(f'Запись {record.id}\n'
                            f'{record.text}')
    else:
        records = modules.record.RecordRepository.read_all(user.chat_id)
        text = ''
        for record in records:
            text = f'{text}\n\nЗапись {record.id}\n' \
                   f'{record.text}'
        await message.reply(text)


@dp.message_handler(commands='del')
@auto_registration
async def del_record(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    record_id = message.text[len('/del'):].strip()
    try:
        record_id = int(record_id)
    except ValueError:
        record_id = None
    if record_id:
        modules.record.RecordRepository.delete(record_id)
        await message.reply('Запись удалена')
    else:
        await message.reply('Запись не найдена')
