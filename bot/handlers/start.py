from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards import get_main_keyboard
from bot.services import user_service
from bot.utils.i18n import _
from bot.models import User

router: Router = Router()

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    user: User = await user_service.get_by_id(message.from_user.id)

    if user is None:
        user = User(
            id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code
        )
        await user_service.save(user)

    await message.answer(_("start", lang=user.language), reply_markup=get_main_keyboard(user.language))
