from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.utils.translation import get_text


async def get_main_reply_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    buttons = await get_text(lang_code, "start_buttons")

    kb_builder = ReplyKeyboardBuilder()

    for button in buttons:
        kb_builder.row(KeyboardButton(text=button))

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )