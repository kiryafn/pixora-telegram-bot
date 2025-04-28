from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from bot.configuration.config import settings

def create_bot() -> Bot:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    return bot