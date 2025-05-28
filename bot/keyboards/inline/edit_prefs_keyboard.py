from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _

def get_view_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for view confirmation.

    Args:
        lang (str): Language code for translating button labels.

    Returns:
        InlineKeyboardMarkup: Keyboard with "Okay" and "Edit" buttons.
    """

    builder = InlineKeyboardBuilder()
    builder.button(text=_("okay", lang=lang), callback_data="confirm:okay")
    builder.button(text=_("edit", lang=lang), callback_data="confirm:edit")
    builder.adjust(2)

    return builder.as_markup()