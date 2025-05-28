from aiogram import Router, F
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.core import logger
from bot.dialogs.set_preferences_dialog import set_prefs_command
from bot.dialogs import EditPreferenceStates
from bot.keyboards import get_view_confirm_keyboard
from bot.services import user_service, job_preference_service
from bot.utils.i18n import _, translator
from bot.models import JobPreference
from bot.utils.photo import get_image_file

router: Router = Router()

@router.message(Command("viewprefs"))
async def view_preferences_handler(message: Message, state: FSMContext) -> None:
    """
    Handle the /viewprefs command:
    - Retrieve the user's language and job preference.
    - If no preference exists, try sending a placeholder image or fallback text.
    - If a preference exists, format and send a summary with an inline confirmation keyboard.
    - Transition FSM to the confirming state.
    """

    lang = await user_service.get_user_lang(message.from_user.id)
    preference : JobPreference = await job_preference_service.get_preference_by_user_id(message.from_user.id)

    if preference is None:
        try:
            photo = get_image_file("noprefs")
            await message.answer_photo(photo=photo, caption=_("no_preferences", lang=lang))
        except (FileNotFoundError, TelegramNetworkError) as e:
            logger.info(f"Cannot send noprefs image: {e}")
            await message.answer(_("no_preferences", lang=lang))
        return

    summary = (
        f"*{_('summary', lang=lang)}*\n\n"
        f"{_('country', lang=lang)}: *{preference.city.country.name}*\n"
        f"{_('city', lang=lang)}: *{preference.city.name}*\n"
        f"{_('title', lang=lang)}: *{preference.title}*\n"
        f"{_('company', lang=lang)}: *{preference.company}*\n"
        f"{_('min_salary', lang=lang)}: *{preference.min_salary}*\n"
    )

    await message.answer(
        summary,
        reply_markup=get_view_confirm_keyboard(lang),
        parse_mode="Markdown")

    await state.set_state(EditPreferenceStates.confirming)

_VIEW_PREFS_BUTTONS = {
    _('view_preferences', lang=lang)
    for lang in translator.translations.keys()
}

@router.message(F.text.in_(_VIEW_PREFS_BUTTONS))
async def prefs_via_button_handler(message: Message, state: FSMContext) -> None:
    """
    Redirect button presses matching 'View Preferences' to the /viewprefs handler.
    """

    await view_preferences_handler(message, state)

@router.callback_query(EditPreferenceStates.confirming, F.data == "confirm:edit")
async def process_edit(callback: CallbackQuery, state: FSMContext):
    """
    Handle the 'Edit' confirmation:
    - Acknowledge the callback.
    - Remove inline keyboard.
    - Clear FSM state.
    - Start the set preferences dialog.
    """

    await callback.answer()
    await callback.message.edit_reply_markup(None)
    await state.clear()
    return await set_prefs_command(callback.message, state)

@router.callback_query(EditPreferenceStates.confirming, F.data == "confirm:okay")
async def process_okay(callback: CallbackQuery):
    """
    Handle the 'Okay' confirmation:
    - Acknowledge the callback.
    - Remove inline keyboard.
    - Send a final acknowledgment message.
    """

    lang = await user_service.get_user_lang(callback.message.chat.id)
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(text=_("all_good", lang=lang), reply_markup=None)
