from .start import router as start_router
from .language import router as language_router
from .help import router as help_router
from .view_preferences import router as view_preferences_router
from .fallback import router as fallback_router
from bot.dialogs import set_preferences_router

routers = [
    start_router,
    language_router,
    help_router,
    view_preferences_router,
    set_preferences_router,
    fallback_router,
]