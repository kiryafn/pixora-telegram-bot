from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _

def get_company_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for company selection.

    Args:
        lang (str): Language code used for translating the button text.

    Returns:
        InlineKeyboardMarkup: Keyboard containing a single "Any company" button.
    """

    builder = InlineKeyboardBuilder()
    builder.button(text=_("Any company", lang=lang), callback_data="company:any")
    builder.adjust(2)

    return builder.as_markup()