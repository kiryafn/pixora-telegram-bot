from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services import user_service
from bot.utils.i18n import _
from bot.models import User

router: Router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    user: User = await user_service.get_by_id(message.from_user.id)
    await message.answer(_("help", lang=user.language))