from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.core.data import AsyncSessionLocal
from bot.core.i18n import _
from bot.keyboards.inline.language_keyboard import get_language_keyboard
from bot.callback_data.language import LanguageCallback
from bot.models import User
from bot.repositories import user_repository

router: Router = Router()

@router.message(Command("language"))
async def language_handler(message: Message) -> None:
    user: User = await user_repository.get_by_id(message.from_user.id)

    await message.answer(
        _("choose_language", lang=user.language),
        reply_markup=get_language_keyboard()
    )

@router.callback_query(LanguageCallback.filter())
async def language_callback_handler(callback: CallbackQuery, callback_data: LanguageCallback) -> None:
    lang_code: str = callback_data.code

    user: User = await user_repository.get_by_id(callback.from_user.id)

    await user_repository.save(
        user_id=user.id,
        username=user.username,
        language=lang_code
    )

    await callback.answer(_("language_changed", lang=user.language))
    await callback.message.edit_text(_("language_changed", lang=user.language))