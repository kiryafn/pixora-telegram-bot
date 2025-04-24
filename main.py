import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.configuration import settings
from bot.core.middleware import LoggingMiddleware
from bot.handlers import register_handlers
from bot.core.logger import logger

async def main() -> None:
    logger.info("🚀 Start Pixora Bot")

    bot = Bot(settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    register_handlers(dp)
    dp.update.middleware(LoggingMiddleware())
    logger.info("✅ Handlers are registered")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("🛑 The bot is stopped and the session is closed")


if __name__ == "__main__":
    asyncio.run(main())