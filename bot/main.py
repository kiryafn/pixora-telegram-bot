import contextlib
import logging
import asyncio
from queue import Queue
from threading import Thread

from bot.configuration.dispatcher import create_dispatcher
from bot.core import logger
from bot.configuration import create_db
from bot.configuration import create_bot
from bot.core.notification_loop import notify_users_about_new_jobs, main_notify_loop
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

        notify_task = asyncio.create_task(main_notify_loop(bot))

        try:
            await dp.start_polling(bot, handle_signals=False)
        finally:
            notify_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await notify_task

            await bot.session.close()
            logger.info("🛑 Bot stopped and session closed")

    asyncio.run(bot_main())

if __name__ == "__main__":
    Thread(target=start_bot, daemon=False).start()
    log_ui.run()