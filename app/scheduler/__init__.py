import asyncio

import app.bot
from app.scheduler.jobs import delete_expire_messages
from configs import bot as bot_configs


async def run():
    """Запускает расписание"""
    while True:
        await delete_expire_messages(
            bot=app.bot.bot,
            expire_message_time=bot_configs.MESSAGE_EXPIRE_TIME,
        )
        await asyncio.sleep(2)
