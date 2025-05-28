from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.callbacks import LanguageCallback

def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for selecting the user language.

    Returns:
        InlineKeyboardMarkup: Keyboard with buttons for each supported language.
    """

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data=LanguageCallback(code="en").pack()),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data=LanguageCallback(code="ru").pack()),
        ],
        [
            InlineKeyboardButton(text="🇵🇱 Polski", callback_data=LanguageCallback(code="pl").pack()),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data=LanguageCallback(code="uk").pack()),
        ],
    ])