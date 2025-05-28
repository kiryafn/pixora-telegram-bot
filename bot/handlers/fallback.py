from aiogram import Router
from aiogram.types import Message

from bot.services import user_service
from bot.utils.i18n import _
from bot.models import User

router: Router = Router()

@router.message()
async def fallback(message: Message) -> None:
    """
    Fallback message handler.

    This handler catches any incoming Message that didn't match other handlers.
    It retrieves the user's language preference and sends a localized
    default response.
    """

    user: User = await user_service.get_by_id(message.from_user.id)
    await message.answer(_("fallback", lang=user.language))
