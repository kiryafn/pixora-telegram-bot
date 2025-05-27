# File: bot/main.py

import logging
import asyncio
from queue import Queue
from threading import Thread

from bot.core import logger
from bot.core.data import create_db
from bot.core.bot import create_bot
from bot.core.dispatcher import create_dispatcher
from bot.middlewares import LoggingMiddleware
from bot.ui.log_window import LogWindow, TkinterLogHandler

log_queue = Queue()
tk_handler = TkinterLogHandler(log_queue)
tk_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(tk_handler)
log_ui = LogWindow(log_queue)

def start_bot():
    async def bot_main():
        logging.basicConfig(level=logging.INFO)
        await create_db()

        bot = create_bot()
        dp = create_dispatcher()
        dp.update.middleware(LoggingMiddleware())
        logger.info("✅ Handlers are registered")

        try:
            await dp.start_polling(bot, handle_signals=False)
        finally:
            await bot.session.close()
            logger.info("🛑 Bot stopped and session closed")

    asyncio.run(bot_main())

if __name__ == "__main__":
    Thread(target=start_bot, daemon=False).start()
    log_ui.run()