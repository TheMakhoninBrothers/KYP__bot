from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked

import new_patch
from app import db
from app import resourses as modules
from configs import bot as bot_settings


class ExtensionBot(Bot):

    async def send_message(self, *args, **kwargs) -> types.Message:
        kwargs['parse_mode'] = 'html'
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
    await bot.send_message(chat_id=283782903, text='123')
    await bot.send_message(
        chat_id=user.chat_id,
        text=f'BOT ID: {user.chat_id}\n'
             f'USERNAME: {user.username}\n'
             'Доступные команды:\n'
             '/start - Главное меню\n'
             '/add - Добавить новую запись\n'
             '/get - Посмотреть все свои записи\n'
             '/get {Номер записи} - Посмотреть в отдельности\n'
             '/del {Номер записи} - Удалить запись\n'
             '/hide - отчистить историю сообщений\n',
    )


@dp.message_handler(commands='add')
@auto_registration
async def add_record(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    new_text = message.html_text[len('/add'):].strip()
    if new_text:
        record = modules.record.schemas.Record(text=new_text,
                                               chat_id=user.chat_id)
        new_record = modules.record.RecordRepository.create(record)
        if new_record:
            await bot.send_message(
                chat_id=user.chat_id,
                text=f'Запись успешно сохранена под номером: {new_record.id}',
            )
    else:
        await bot.send_message(
            chat_id=user.chat_id,
            text='Вам нужно добавить текст после /add\n'
                 'Например: "/add Моя новая запись"',
        )


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


@dp.message_handler(commands='hide')
@auto_registration
async def hide_all_message_history(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    await modules.user.MessageHistoryController(message).clear_history_bot()
    await bot.send_message(
        chat_id=user.chat_id,
        text=f'BOT ID: {user.chat_id}\n'
             f'USERNAME: {user.username}\n'
             'Доступные команды:\n'
             '/start - Главное меню\n'
             '/add - Добавить новую запись\n'
             '/get - Посмотреть все свои записи\n'
             '/get {Номер записи} - Посмотреть в отдельности\n'
             '/del {Номер записи} - Удалить запись\n'
             '/hide - отчистить историю сообщений\n',
    )


@dp.message_handler(regexp=bot_settings.SEARCH_TAGS_REGEX)
@auto_registration
async def search_by_tags(message: types.Message, user: modules.user.schemas.UserBotFromDB):
    """Поиск по тегам"""
    tags = modules.helpers.parse_tags(message.text, bot_settings.SEARCH_TAGS_REGEX)
    records = modules.record.RecordSearcher(str(message.chat.id)).by_tags(*tags)
    if records:
        text = ''
        for record in records:
            text = f'{text}\n\nЗапись {record.id}\n' \
                   f'{record.text}'
        await bot.send_message(chat_id=user.chat_id, text=text)
    else:
        text_tags = ' '.join([f'#{item}' for item in tags])
        await bot.send_message(
            chat_id=user.chat_id,
            text=f'Данные не найдены\n'
                 f'Теги поиска: {text_tags}',
        )


@dp.errors_handler(exception=BotBlocked)
async def disable_user(update: types.Update, exc: BotBlocked):
    user: db.TelegramUser = db.Session().query(db.TelegramUser).filter_by(telegram_id=str(update.message.chat.id)).one()
    user.is_able = False
    db.Session().commit()
    return True
