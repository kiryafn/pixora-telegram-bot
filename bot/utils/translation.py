import json
from pathlib import Path
from typing import Any

import aiofiles

from data.models.user import User
from data.repositories.user_repository import user_repository


async def get_text(lang_code: str, text_name: str):
    supported_langs = {"ru", "en", "pl", "uk"}
    lang = lang_code if lang_code in supported_langs else "en"

    #file_path = Path.cwd() / "data" / "locales" / f"{lang}.json"
    file_path = f"/Users/alieksieiev/PycharmProjects/pixora-telegram-bot/data/locales/{lang}.json"

    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
        return json.loads(content).get(text_name)