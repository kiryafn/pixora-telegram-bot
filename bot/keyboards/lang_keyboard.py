from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.translation import get_text

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.translation import get_text


async def get_main_reply_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    buttons = await get_text(lang_code, "start_buttons")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons[0])],  # 🌐 Change language
            [KeyboardButton(text=buttons[1])]   # ⚙️ Set preferences
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="👇 Выберите действие"
    )
    return keyboard