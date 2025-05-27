# language: python
import os
from aiogram.types import FSInputFile
from bot.core import logger

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGES_DIR = os.path.join(BASE_DIR, "data", "img")

def get_image_path(name: str, ext: str = "png") -> str:
    """
    Возвращает абсолютный путь до изображения по его имени (без расширения).
    Бросает FileNotFoundError, если файл не найден.
    """
    filename = f"{name}.{ext}"
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        logger.error(f"Image not found: {path}")
        raise FileNotFoundError(f"Image '{filename}' not found in {IMAGES_DIR}")
    return path

def get_image_file(name: str, ext: str = "png") -> FSInputFile:
    """
    Создаёт и возвращает FSInputFile для отправки через aiogram.
    """
    path = get_image_path(name, ext)
    return FSInputFile(path)