import logging
import threading
import queue
import tkinter as tk

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.services import user_service

logger = logging.getLogger('pixora')

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user = event.message.from_user
            text = event.message.text or "<non-text message>"
            lang = await user_service.get_user_lang(user.id)
            log_msg = (
                f"📥 Message from {user.full_name} "
                f"(@{user.username}) [LANG: {lang}] [ID: {user.id}]: {text}"
            )
            logger.info(log_msg)
        return await handler(event, data)