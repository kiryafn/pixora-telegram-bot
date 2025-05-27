from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.services import user_service
from bot.core import logger

DEFAULT_LANG = "en"

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user = event.message.from_user
            text = event.message.text or "<non-text message>"

            try:
                lang = await user_service.get_user_lang(user.id) or DEFAULT_LANG
            except Exception as e:
                logger.warning(f"Can't fetch language for user {user.id}: {e}")
                lang = DEFAULT_LANG

            log_msg = (
                f"📥 Message from {user.full_name} "
                f"(@{user.username}) [LANG: {lang}] [ID: {user.id}]: {text}"
            )
            logger.info(log_msg)

        return await handler(event, data)