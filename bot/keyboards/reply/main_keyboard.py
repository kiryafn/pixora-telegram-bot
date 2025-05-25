from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils.i18n import _


def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=_('set_preferences', lang=lang))
    builder.button(text=_('view_preferences', lang=lang))
    builder.button(text=_('language', lang=lang))
    builder.button(text=_('terms_and_policy', lang=lang))

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
