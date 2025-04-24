from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards import get_language_inline_keyboard, get_main_reply_keyboard
from data.repositories.user_repository import user_repository
from bot.utils.translation import get_text
from data.supported_languages import LANG_CODES
router = Router()

@router.message(F.text.in_(["Change language", "Zmień język", "Сменить язык", "Змінити мову"]))
async def cmd_start(message: Message) -> None:
    from_user = message.from_user
    lang = await user_repository.get_user_lang(from_user.id)
    text = await get_text(lang, "choose_language")
    keyboard = await get_language_inline_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.in_(LANG_CODES))
async def language_chosen(callback: CallbackQuery):
    new_lang = callback.data
    user_id  = callback.from_user.id

    user = await user_repository.get_by_id(user_id)
    if user:
        user.language_code = new_lang
        await user_repository.save(user)

    text = await get_text(new_lang, "language_changed")

    await callback.answer(text, show_alert=True)

    main_kb  = await get_main_reply_keyboard(new_lang)

    #await callback.message.edit_text(text)
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=main_kb)