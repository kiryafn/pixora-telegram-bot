from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_city_keyboard(cities: list, page: int = 1) -> InlineKeyboardMarkup:
    ITEMS_PER_PAGE = 9
    total_pages = (len(cities) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    page = max(1, min(page, total_pages))

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    current_chunk = cities[start:end]

    builder = InlineKeyboardBuilder()
    for city in current_chunk:
        builder.button(
            text=city.name,
            callback_data=f"city:{city.id}"
        )
    builder.adjust(3)

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️", callback_data=f"page:{page-1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="▶️", callback_data=f"page:{page+1}")
        )

    if nav_buttons:
        builder.row(*nav_buttons)

    return builder.as_markup()