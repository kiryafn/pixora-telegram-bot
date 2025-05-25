from .start import router as start_router
from .language import router as language_router
from .help import router as help_router
from .view_preferences import router as view_preferences_router
from .fallback import router as fallback_router
from bot.dialogs.set_preferences_dialog import router as preferences_dialog_router

routers = [
    start_router,
    language_router,
    help_router,
    view_preferences_router,
    preferences_dialog_router,
    fallback_router,
]