from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _


def get_link_keyboard(lang: str, url: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=_("job_url", lang=lang), url=url)

    return builder.as_markup()