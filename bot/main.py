import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.configuration import settings
from bot.core.middleware import LoggingMiddleware
from bot.handlers import register_handlers


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("🚀 Запускаем Pixora Bot")

    # 2) Инициализируем Bot и Dispatcher
    bot = Bot(settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # 3) Регистрируем все роутеры
    register_handlers(dp)
    dp.update.middleware(LoggingMiddleware())
    logger.info("✅ Handlers are registered")

    # 4) Стартуем polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("🛑 The bot is stopped and the session is closed")


if __name__ == "__main__":
    asyncio.run(main())