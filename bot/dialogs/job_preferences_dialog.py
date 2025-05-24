from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.company_keyboard import get_company_keyboard
from bot.keyboards.inline.confirm_keyboard import get_confirm_keyboard
from bot.keyboards.inline.country_keyboard import get_country_keyboard
from bot.keyboards.inline.city_keyboard import get_city_keyboard
from bot.models import JobPreference
from bot.services import country_service, city_service
from bot.dialogs.states.job_preference_states import JobPreferenceStates
from bot.utils.i18n import _
from bot.services import user_service

router = Router()

@router.message(Command("setprefs"))
async def set_prefs_command(message: Message, state: FSMContext):
    lang = await user_service.get_user_lang(message.from_user.id)
    await state.clear()

    await message.answer(
        _("choose_country", lang=lang),
        reply_markup=await get_country_keyboard(lang)
    )
    await state.set_state(JobPreferenceStates.waiting_for_country)


@router.callback_query(JobPreferenceStates.waiting_for_country, F.data.startswith("country:"))
async def country_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    country_id = int(callback.data.split(":", 1)[1])
    country = await country_service.get_by_id(country_id)
    await state.update_data(country_id=country.id, country_name=country.name)

    await callback.message.edit_text(
        _("selected_country", lang=lang).format(country=country.name),
        reply_markup=None
    )

    cities = await city_service.get_all_cities_by_country(country.name)
    if not cities:
        return await callback.message.answer(_("no_cities_in_country", lang=lang))

    await callback.message.answer(
        _("choose_city", lang=lang),
        reply_markup=get_city_keyboard(cities, page=1)
    )
    await state.set_state(JobPreferenceStates.waiting_for_city)


@router.callback_query(JobPreferenceStates.waiting_for_city, F.data.startswith("page:"))
async def paginate_cities(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    data = await state.get_data()
    cities = await city_service.get_all_cities_by_country(data.get("country_name"))
    new_page = int(callback.data.split(":", 1)[1])

    await callback.message.edit_reply_markup(
        reply_markup=get_city_keyboard(cities, lang, page=new_page)
    )


@router.callback_query(JobPreferenceStates.waiting_for_city, F.data.startswith("city:"))
async def city_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    city_id = int(callback.data.split(":", 1)[1])
    city = await city_service.get_by_id(city_id)
    await state.update_data(city_id=city.id, city_name=city.name)

    await callback.message.edit_text(
        _("selected_city", lang=lang).format(city=city.name),
        reply_markup=None
    )

    await callback.message.answer(_("enter_title", lang=lang))
    await state.set_state(JobPreferenceStates.waiting_for_title)


@router.message(JobPreferenceStates.waiting_for_title)
async def title_chosen(message: Message, state: FSMContext):
    lang = await user_service.get_user_lang(message.from_user.id)
    await state.update_data(title=message.text)
    # Отправляем inline-клавиатуру с кнопкой "Any company"
    await message.answer(
        _("enter_company", lang=lang),
        reply_markup=get_company_keyboard(lang)
    )
    await state.set_state(JobPreferenceStates.waiting_for_company)


# Новый хэндлер для кнопки "Any company"
@router.callback_query(JobPreferenceStates.waiting_for_company, F.data == "company:any")
async def any_company_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)
    # Сохраняем company = NULL
    await state.update_data(company=None, company_name=_("any", lang=lang))
    data = await state.get_data()
    # Убираем inline-клавиатуру
    await callback.message.edit_text(text=_("selected_any_company", lang=lang).format(any=data["company_name"]), reply_markup=None)
    await callback.message.answer(_("enter_min_salary", lang=lang))
    await state.set_state(JobPreferenceStates.waiting_for_min_salary)


@router.message(JobPreferenceStates.waiting_for_company)
async def company_chosen(message: Message, state: FSMContext):
    # Этот хэндлер срабатывает, если пользователь вводит текст вручную
    lang = await user_service.get_user_lang(message.from_user.id)
    await state.update_data(company=message.text, company_name=message.text)
    await message.answer(_("enter_min_salary", lang=lang))
    await state.set_state(JobPreferenceStates.waiting_for_min_salary)



@router.message(JobPreferenceStates.waiting_for_min_salary)
async def min_sal_chosen(message: Message, state: FSMContext):
    lang = await user_service.get_user_lang(message.from_user.id)

    if not message.text.isdigit():
        return await message.answer(_("error_digits_only", lang=lang))

    await state.update_data(min_salary=float(message.text))
    data = await state.get_data()

    summary = (
        f"*{_('summary', lang=lang)}*\n\n"
        f"{_('country', lang=lang)}: *{data['country_name']}*\n"
        f"{_('city', lang=lang)}: *{data['city_name']}*\n"
        f"{_('title', lang=lang)}: *{data['title']}*\n"
        f"{_('company', lang=lang)}: *{data['company_name']}*\n"
        f"{_('min_salary', lang=lang)}: *{data['min_salary']}*\n"
    )

    await message.answer(
        summary,
        reply_markup=get_confirm_keyboard(lang),
        parse_mode="Markdown"
    )
    await state.set_state(JobPreferenceStates.confirming)


@router.callback_query(JobPreferenceStates.confirming, F.data == "confirm:yes")
async def process_save(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # получаем язык перевода
    user = await user_service.get_by_id(callback.from_user.id)
    lang = user.language

    data = await state.get_data()
    from bot.models.user import User
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from bot.core.data import async_session

    async with async_session() as session:
        # заранее подгружаем job_preferences, чтобы не было lazy-load
        stmt = (
            select(User)
            .options(selectinload(User.job_preferences))
            .where(User.id == callback.from_user.id)
        )
        result = await session.execute(stmt)
        db_user = result.scalar_one()

        # создаём новую запись JobPreference и сразу её добавляем в эту же сессию
        pref = JobPreference(
            title=data["title"],
            company=data["company"] if data["company"] else None,
            min_salary=data["min_salary"],
            city_id=data["city_id"]
        )
        session.add(pref)

        # привязываем предпочтение к пользователю
        db_user.job_preferences.append(pref)

        # фиксируем всё сразу
        await session.commit()

    # отвечаем пользователю об успехе
    await callback.message.edit_reply_markup(None)
    await callback.message.answer(_("saved_successfully", lang=lang))
    await state.clear()


@router.callback_query(JobPreferenceStates.confirming, F.data == "confirm:no")
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    await callback.message.edit_reply_markup(None)
    await callback.message.answer(_("operation_cancelled", lang=lang))
    await state.clear()