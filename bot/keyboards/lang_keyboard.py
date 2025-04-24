from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.utils.translation import get_text
from data.supported_languages import Language

async def get_main_reply_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    buttons = await get_text(lang_code, "start_buttons")

    kb_builder = ReplyKeyboardBuilder()

    for button in buttons:
        kb_builder.row(KeyboardButton(text=button))

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

async def get_language_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for language in Language:
        builder.button(text=language.value, callback_data=language.name)

    builder.adjust(2)
    return builder.as_markup()