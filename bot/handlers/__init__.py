from aiogram import Dispatcher
from .common import router as common_router
from .language_chooser import router as language_router
#from .jobs import setup_dialog

"""
    Include all routers into Dispatcher.
"""
def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(language_router)
    dp.include_router(common_router)
    #setup_dialog(dp)

__all__ = "register_handlers"