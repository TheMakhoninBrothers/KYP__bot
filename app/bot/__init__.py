from aiogram import Bot, Dispatcher, types

import new_patch
from app import db
from app import resourses as modules
from configs import bot as bot_settings


class ExtensionBot(Bot):

    async def send_message(self, *args, **kwargs) -> types.Message:
        message = await super(ExtensionBot, self).send_message(*args, **kwargs)
        await save_user_step(message)
        return message


async def save_user_step(message: types.Message):
    user_step = db.UserHistory(chat_id=message.chat.id,
                               message_id=message.message_id,
                               )
    db.Session().add(user_step)
    db.Session().commit()
    db.Session().close()


bot = ExtensionBot(token=bot_settings.TOKEN)

dp = Dispatcher(bot)


async def on_startup(dispatcher, url=None, cert=None):
    for user in modules.user.repository.TelegramUserRepository.read_all():
        await bot.send_message(chat_id=user.chat_id, text='Бот запущен')
        await bot.send_message(chat_id=user.chat_id, text=new_patch.text)


async def on_shutdown(dispatcher):
    for user in modules.user.repository.TelegramUserRepository.read_all():
        await bot.send_message(chat_id=user.chat_id, text='Бот выключился')


def auto_registration(func):
    async def wrapper(message: types.Message):
        if modules.user.TelegramUserRepository.is_exist(str(message.chat.id)):
            user = modules.user.TelegramUserRepository.read(str(message.chat.id))
        else:
            user = modules.user.schemas.UserBot(username=message.chat.username,
                                                chat_id=message.chat.id,
                                                )
            user = modules.user.TelegramUserRepository.create(user)
        await save_user_step(message)
        return await func(message, user)

    return wrapper


@dp.message_handler(commands='start')
@auto_registration
async def main_menu(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    await bot.send_message(chat_id=user.chat_id,
                           text=f'BOT ID: {user.chat_id}\n'
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
            await bot.send_message(chat_id=user.chat_id,
                                   text=f'Запись успешно сохранена под номером: {new_record.id}')
    else:
        await bot.send_message(chat_id=user.chat_id,
                               text='Вам нужно добавить текст после /add\n'
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
        await bot.send_message(chat_id=user.chat_id, text=text)


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
        await bot.send_message(chat_id=user.chat_id, text='Запись удалена')
    else:
        await bot.send_message(chat_id=user.chat_id, text='Запись не найдена')
