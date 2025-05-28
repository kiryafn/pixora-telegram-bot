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
    """
    Handle the /language command.

    Retrieves the user's current language setting and sends
    a prompt with an inline keyboard for choosing a new language.
    """

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
    """
    Handle text-based language selection buttons.

    If the user taps a localized "Language" button,
    this reuses the same logic as the /language command handler.
    """

    await language_handler(message)

@router.callback_query(LanguageCallback.filter())
async def language_callback_handler(callback: CallbackQuery, callback_data: LanguageCallback) -> None:
    """
    Handle an inline callback when the user selects a new language.

    Args:
        callback (CallbackQuery): The callback query object containing
            information about the original message and the user.
        callback_data (LanguageCallback): Parsed callback data, including
            the `code` attribute with the selected language code.

    Workflow:
        1. Extract the language code from `callback_data.code`.
        2. Retrieve the User model by `callback.from_user.id`.
        3. Update and persist the user's `language` preference.
        4. Acknowledge the callback without sending a visible notification.
        5. Delete the original message containing the language selection UI.
        6. Send a confirmation message with the main keyboard localized to the new language.
    """

    lang_code: str = callback_data.code

    user: User = await user_service.get_by_id(callback.from_user.id)
    user.language = lang_code
    await user_service.save(user)

    await callback.answer(_("language_changed", lang=lang_code))

    await callback.message.delete()

    await callback.message.answer(_("language_changed", lang=lang_code), reply_markup=get_main_keyboard(lang_code)
    )
