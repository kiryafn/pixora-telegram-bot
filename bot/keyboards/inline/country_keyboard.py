from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.i18n import _
from bot.services.country_service import country_service

async def get_country_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
   Build an inline keyboard listing all countries.

   Args:
       lang (str): Language code to use for button labels.

   Returns:
       InlineKeyboardMarkup: Keyboard with one button per country.
   """

    countries = await country_service.get_all()

    builder = InlineKeyboardBuilder()
    for country in countries:
        key = f"country_{country.name.lower()}"
        translation = _(key, lang=lang)
        text = translation if translation != key else country.name
        builder.button(
            text=text,
            callback_data=f"country:{country.id}"
        )

    builder.adjust(2)
    return builder.as_markup()