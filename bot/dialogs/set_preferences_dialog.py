from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from bot.keyboards import get_company_keyboard
from bot.keyboards import get_confirm_keyboard
from bot.keyboards import get_country_keyboard
from bot.keyboards import get_city_keyboard
from bot.services import country_service, city_service, user_service
from bot.dialogs import SetPreferenceStates
from bot.utils.i18n import _, translator
from bot.configuration.database import async_session
from bot.models.job_preference import JobPreference


router = Router()

@router.message(Command("setprefs"))
async def set_prefs_command(message: Message, state: FSMContext):
    """
    Handle /setprefs command.
    Prompts the user to choose a country and sets the FSM state to waiting_for_country.
    """

    lang = await user_service.get_user_lang(message.chat.id)
    await state.clear()

    await message.answer(
        _("choose_country", lang=lang),
        reply_markup=await get_country_keyboard(lang)
    )
    await state.set_state(SetPreferenceStates.waiting_for_country)

_SET_PREFS_BUTTONS = {
    _('set_preferences', lang=lang)
    for lang in translator.translations.keys()
}

@router.message(F.text.in_(_SET_PREFS_BUTTONS))
async def prefs_via_button_handler(message: Message, state: FSMContext) -> None:
    """
    Redirects button-based "Set Preferences" requests to the same command handler.
    """

    await set_prefs_command(message, state)


@router.callback_query(SetPreferenceStates.waiting_for_country, F.data.startswith("country:"))
async def country_chosen(callback: CallbackQuery, state: FSMContext):
    """
    Handle country selection callback.
    Saves the chosen country in FSM data, updates the message,
    and prompts the user to choose a city.
    """

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
    await state.set_state(SetPreferenceStates.waiting_for_city)


@router.callback_query(SetPreferenceStates.waiting_for_city, F.data.startswith("page:"))
async def paginate_cities(callback: CallbackQuery, state: FSMContext):
    """
    Handle pagination buttons for city list.
    Updates inline keyboard to show the requested page of cities.
    """

    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    data = await state.get_data()
    cities = await city_service.get_all_cities_by_country(data.get("country_name"))
    new_page = int(callback.data.split(":", 1)[1])

    await callback.message.edit_reply_markup(
        reply_markup=get_city_keyboard(cities, page=new_page)
    )


@router.callback_query(SetPreferenceStates.waiting_for_city, F.data.startswith("city:"))
async def city_chosen(callback: CallbackQuery, state: FSMContext):
    """
    Handle city selection callback.
    Saves the chosen city in FSM data, updates the message,
    and prompts the user to enter a job title.
    """

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
    await state.set_state(SetPreferenceStates.waiting_for_title)


@router.message(SetPreferenceStates.waiting_for_title)
async def title_chosen(message: Message, state: FSMContext):
    """
    Handle job title input.
    Saves the entered title in FSM data and prompts the user to choose or enter a company.
    """

    lang = await user_service.get_user_lang(message.from_user.id)
    await state.update_data(title=message.text)
    # Отправляем inline-клавиатуру с кнопкой "Any company"
    await message.answer(
        _("enter_company", lang=lang),
        reply_markup=get_company_keyboard(lang)
    )
    await state.set_state(SetPreferenceStates.waiting_for_company)


@router.callback_query(SetPreferenceStates.waiting_for_company, F.data == "company:any")
async def any_company_chosen(callback: CallbackQuery, state: FSMContext):
    """
    Handle "Any company" selection.
    Records a null company preference, updates the message,
    and prompts the user to enter minimum salary.
    """

    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    await state.update_data(company=None, company_name=_("any", lang=lang))
    data = await state.get_data()

    await callback.message.edit_text(text=_("selected_any_company", lang=lang).format(any=data["company_name"]), reply_markup=None)
    await callback.message.answer(_("enter_min_salary", lang=lang))
    await state.set_state(SetPreferenceStates.waiting_for_min_salary)


@router.message(SetPreferenceStates.waiting_for_company)
async def company_chosen(message: Message, state: FSMContext):
    """
    Handle manual company name input.
    Saves the entered company name and prompts the user to enter minimum salary.
    """

    lang = await user_service.get_user_lang(message.from_user.id)
    await state.update_data(company=message.text, company_name=message.text)
    await message.answer(_("enter_min_salary", lang=lang))
    await state.set_state(SetPreferenceStates.waiting_for_min_salary)



@router.message(SetPreferenceStates.waiting_for_min_salary)
async def min_sal_chosen(message: Message, state: FSMContext):
    """
    Handle minimum salary input.
    Validates numeric input, saves it in FSM data,
    then shows a summary and asks for confirmation.
    """

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
    await state.set_state(SetPreferenceStates.confirming)


@router.callback_query(SetPreferenceStates.confirming, F.data == "confirm:yes")
async def process_save(callback: CallbackQuery, state: FSMContext):
    """
    Handle confirmation to save preferences.
    Inserts or updates the JobPreference record in the database,
    then notifies the user of success.
    """

    await callback.answer()
    user = await user_service.get_by_id(callback.from_user.id)
    lang = user.language

    data = await state.get_data()

    async with async_session() as session:
        stmt = select(JobPreference).where(JobPreference.user_id == callback.from_user.id)
        result = await session.execute(stmt)
        pref = result.scalar_one_or_none()

        if pref is None:
            pref = JobPreference(
                user_id=callback.from_user.id,
                title=data["title"],
                company=data["company"] or None,
                min_salary=data["min_salary"],
                city_id=data["city_id"],
            )
            session.add(pref)
        else:
            pref.title = data["title"]
            pref.company = data["company"] or None
            pref.min_salary = data["min_salary"]
            pref.city_id = data["city_id"]

        await session.commit()

    await callback.message.edit_reply_markup(None)
    await callback.message.answer(_("saved_successfully", lang=lang))
    await state.clear()


@router.callback_query(SetPreferenceStates.confirming, F.data == "confirm:no")
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Handle cancellation of preference setup.
    Clears the FSM state and notifies the user that the operation was cancelled.
    """

    await callback.answer()
    lang = await user_service.get_user_lang(callback.from_user.id)

    await callback.message.edit_reply_markup(None)
    await callback.message.answer(_("operation_cancelled", lang=lang))
    await state.clear()