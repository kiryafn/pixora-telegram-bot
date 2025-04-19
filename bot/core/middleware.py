# bot/core/middlewares.py

import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        # Логируем текстовые сообщения от пользователя
        if event.message:
            user = event.message.from_user
            text = event.message.text or "<non-text message>"
            logger.info(
                f"📥 Message from {user.full_name} (@{user.username}) [LANG: {user.language_code}] [ID: {user.id}]: {text}"
            )
        return await handler(event, data)
