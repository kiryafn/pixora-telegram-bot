import asyncio
import logging
#from dotenv import load_dotenv

from bot.core.data import create_db

#load_dotenv()

from bot.core.bot import create_bot
from bot.core.dispatcher import create_dispatcher

async def main():
    logging.basicConfig(level=logging.INFO)

    await create_db()

    bot = create_bot()
    dp = create_dispatcher()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())