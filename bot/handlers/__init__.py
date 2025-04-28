from .start import router as start_router
from .language import router as language_router
from .help import router as help_router
from .fallback import router as fallback_router

routers = [
    start_router,
    language_router,
    help_router,
    fallback_router,
]