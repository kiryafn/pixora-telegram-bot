from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _

def get_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=_("yes", lang=lang), callback_data="confirm:yes")
    builder.button(text=_("no", lang=lang), callback_data="confirm:no")
    builder.adjust(2)

    return builder.as_markup()