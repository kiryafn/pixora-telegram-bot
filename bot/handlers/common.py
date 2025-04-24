from aiogram import Router
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message, FSInputFile

from bot.keyboards.lang_keyboard import get_main_reply_keyboard
from data.models.user import User
from data.repositories.user_repository import user_repository
from bot.utils.translation import get_text
from aiogram import F
from bot.core.logger import logger

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    from_user = message.from_user

    user = await user_repository.get_by_id(from_user.id)

    if not user:
        new_user = User(id=from_user.id, username=from_user.username, language_code=from_user.language_code, full_name=from_user.full_name)
        await user_repository.save(new_user)
        logger.info(f"🧝🏻‍♀️ New user {new_user.id}: added to db")

    lang = await user_repository.get_user_lang(from_user.id)
    text = await get_text(lang, "start")
    keyboard = await get_main_reply_keyboard(lang)

    await message.answer(text, reply_markup=keyboard)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = await get_text(await user_repository.get_user_lang(message.from_user.id), "help")
    await message.answer(text)

@router.message(F.text == "🤡")
async def clown_reply(message: Message) -> None:
    await message.answer("Сам клоун")
    await message.answer("🤡")

@router.message()
async def fallback(message: Message) -> None:
    text = await get_text(await user_repository.get_user_lang(message.from_user.id), "fallback")
    await message.answer(text)