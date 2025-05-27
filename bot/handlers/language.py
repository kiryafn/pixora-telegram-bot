from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards import get_main_keyboard
from bot.services import user_service
from bot.utils.i18n import _, translator
from bot.keyboards import get_language_keyboard
from bot.callbacks import LanguageCallback
from bot.models import User

router: Router = Router()

@router.message(Command("language"))
async def language_handler(message: Message) -> None:
    user: User = await user_service.get_by_id(message.from_user.id)

    await message.answer(
        _("choose_language", lang=user.language),
        reply_markup=get_language_keyboard()
    )

_LANGUAGE_BUTTONS = {
    _('language', lang=lang)
    for lang in translator.translations.keys()
}

@router.message(F.text.in_(_LANGUAGE_BUTTONS))
async def language_via_button_handler(message: Message) -> None:
    await language_handler(message)

@router.callback_query(LanguageCallback.filter())
async def language_callback_handler(callback: CallbackQuery, callback_data: LanguageCallback) -> None:
    lang_code: str = callback_data.code

    user: User = await user_service.get_by_id(callback.from_user.id)
    user.language = lang_code
    await user_service.save(user)

    await callback.answer(_("language_changed", lang=lang_code))

    await callback.message.delete()

    await callback.message.answer(_("language_changed", lang=lang_code), reply_markup=get_main_keyboard(lang_code)
    )
