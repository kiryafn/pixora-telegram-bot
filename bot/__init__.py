import logging
from .config import BOT_TOKEN

__version__ = "0.1.0"

logger = logging.getLogger("pixora_telegram_bot")
logger.setLevel(logging.INFO)
logger.info(f"Launch of Bot Package, version {__version__}")

# Удобный экспорт ключевых объектов
__all__ = [
    "BOT_TOKEN",
    "logger",
    "__version__",
]