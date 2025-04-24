# bot/handlers/__init__.py

from aiogram import Dispatcher

from .common import router as common_router
from .language_chooser import router as language_router

__all__ = ("register_handlers",)

def register_handlers(dp: Dispatcher) -> None:
    """
    Include all routers into Dispatcher.
    """
    dp.include_router(language_router)
    dp.include_router(common_router)
