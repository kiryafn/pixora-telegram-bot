from aiogram import Router
from aiogram.types import Message

from bot.core.data import AsyncSessionLocal
from bot.core.i18n import _
from bot.models import User
from bot.repositories import user_repository

router: Router = Router()


@router.message()
async def fallback(message: Message) -> None:

    user: User = await user_repository.get_user_by_id(message.from_user.id)
    await message.answer(_("fallback", lang=user.language))
