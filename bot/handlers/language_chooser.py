from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from data.models.user import User
from data.repositories.user_repository import user_repository
from bot.utils.translation import get_text, get_lang

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    from_user = message.from_user

    user = await user_repository.get_by_id(from_user.id)

    if not user:
        new_user = User(id=from_user.id, username=from_user.username, language_code=from_user.language_code, full_name=from_user.full_name)
        await user_repository.save(new_user)
        print(f"New user added {new_user.id}: added to db")

    text = await get_text(await get_lang(message.from_user.id), "start")
    await message.answer(text)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = await get_text(await get_lang(message.from_user.id), "help")
    await message.answer(text)

@router.message()
async def fallback(message: Message) -> None:
    text = await get_text(await get_lang(message.from_user.id), "fallback")
    await message.answer(text)