from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services import user_service
from bot.utils.i18n import _
from bot.models import User

router: Router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """
    Handle the /help command.

    This handler is triggered when a user sends the /help command.
    It looks up the user's language preference and sends back
    a localized help message explaining available bot commands.
    """

    user: User = await user_service.get_by_id(message.from_user.id)
    await message.answer(_("help", lang=user.language))