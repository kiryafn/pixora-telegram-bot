import asyncio
import logging
# from dotenv import load_dotenv

from bot.core.data import create_db
# load_dotenv()

from bot.core.bot import create_bot
from bot.core.dispatcher import create_dispatcher

from bot.scheduler.jobs import start_scheduler


async def main():
    logging.basicConfig(level=logging.INFO)

    # 1) Инициализируем базу
    await create_db()

    # 2) Запускаем наш планировщик (работает в том же asyncio-loop)
    start_scheduler()

    # 3) Запускаем бота
    bot = create_bot()
    dp = create_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
