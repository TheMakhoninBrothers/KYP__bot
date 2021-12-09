import asyncio

import app.bot
from app.scheduler.jobs import delete_expire_message
from configs import bot as bot_configs


async def main():
    while True:
        await delete_expire_message(bot=app.bot.bot,
                                    expire_message_time=bot_configs.MESSAGE_EXPIRE_TIME,
                                    )
        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
