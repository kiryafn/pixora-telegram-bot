from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.core.i18n import _
from bot.models import User
from bot.repositories import user_repository

router: Router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    user: User = await user_repository.get_user_by_id(message.from_user.id)

    if not user:
        user = await user_repository.create_user(
            user_id=message.from_user.id,
            username=message.from_user.username or "Anonymous",
            language=message.from_user.language_code or "en"
        )

    await message.answer(_("start", lang=user.language))
