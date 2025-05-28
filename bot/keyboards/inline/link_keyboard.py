from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.i18n import _


def get_link_keyboard(lang: str, url: str):
    """
    Create an inline keyboard with a single link button.

    Args:
        lang (str): Language code for the button label.
        url (str): URL to open when the button is pressed.

    Returns:
        InlineKeyboardMarkup: Keyboard containing the link button.
    """

    builder = InlineKeyboardBuilder()
    builder.button(text=_("job_url", lang=lang), url=url)

    return builder.as_markup()