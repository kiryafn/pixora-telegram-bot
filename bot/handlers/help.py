from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.data import AsyncSessionLocal
from bot.core.i18n import _
from bot.models import User
from bot.repositories.user_repository import UserRepository

router: Router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_repository: UserRepository = UserRepository(session)
        user: User = await user_repository.get_user_by_id(message.from_user.id)

    await message.answer(_("help", lang=user.language))