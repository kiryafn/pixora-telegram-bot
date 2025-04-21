# bot/core/middlewares.py

import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

from data.repositories.user_repository import user_repository

logger = logging.getLogger('pixora')

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user = event.message.from_user
            text = event.message.text or "<non-text message>"
            logger.info(
                f"📥 Message from {user.full_name} (@{user.username}) [LANG: {await user_repository.get_user_lang(user.id)}] [ID: {user.id}]: {text}"
            )
        return await handler(event, data)
