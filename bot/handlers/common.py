from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.testing.suite.test_reflection import users

from bot.models.user import User
from bot.core.db import async_session
from sqlalchemy import select
import json
import os

from bot.services.repository.user_repository import UserRepository

router = Router()

def get_translations(lang_code: str) -> dict:

    supported_langs = {"ru", "en", "pl", "uk"}
    lang = lang_code if lang_code in supported_langs else "en"
    file_path = f"/Users/alieksieiev/PycharmProjects/pixora-telegram-bot/data/locales/{lang}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    from_user = message.from_user

    user = await UserRepository.get_by_id(from_user.id)

    if not user:
        new_user = User(
            id=from_user.id,
            username=from_user.username,
            language_code=from_user.language_code
        )
        await UserRepository.save(new_user)
        print(f"new user added {new_user.id}: added to db")

    text = get_translations(from_user.language_code).get("greeting")

    await message.answer(text)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "🛠 Список доступных команд:\n"
        "/start — приветствие и краткая инструкция\n"
        "/help — это сообщение\n"
        "/setprefs — задать или изменить параметры поиска\n"
        "/jobs — получить свежие вакансии"
    )
@router.message()
async def fallback(message: Message):
    await message.answer("❓ Я пока не знаю такой команды. Попробуй /help")