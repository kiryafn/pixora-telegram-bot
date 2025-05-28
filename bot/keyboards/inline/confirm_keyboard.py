from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _

def get_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Create a confirmation inline keyboard with "Yes" and "No" options.

    Args:
        lang (str): Language code for translating button labels.

    Returns:
        InlineKeyboardMarkup: Keyboard with two buttons for confirmation.
    """

    builder = InlineKeyboardBuilder()
    builder.button(text=_("yes", lang=lang), callback_data="confirm:yes")
    builder.button(text=_("no", lang=lang), callback_data="confirm:no")
    builder.adjust(2)

    return builder.as_markup()