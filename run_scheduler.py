import asyncio

from app import scheduler


async def main():
    """Точка входа"""
    await scheduler.run()


if __name__ == '__main__':
    asyncio.run(main())
