from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.supported_languages import Language

async def get_language_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for language in Language:
        builder.button(text=language.value, callback_data=language.name)

    builder.adjust(2)
    return builder.as_markup()