import json
from pathlib import Path
from typing import Any, List

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

def get_all_by_key(
    key: str
) -> List[Any]:
    """
    Сканирует все .json файлы в директории dir_path и собирает значение key из каждого файла.

    :param dir_path: путь к директории с JSON-файлами локализации
    :param key: ключ, значение по которому нужно извлечь из каждого файла
    :return: список значений, найденных по ключу; если в каком-то файле ключ отсутствует — он пропускается
    """
    values: List[Any] = []
    dir_path = Path("/Users/alieksieiev/PycharmProjects/pixora-telegram-bot/data/locales")

    if not dir_path.is_dir():
        raise ValueError(f"Путь {dir_path!r} не является директорией")

    for json_file in dir_path.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            continue

        if key in data:
            values.append(data[key])

    return values