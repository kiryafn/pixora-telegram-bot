from aiogram.fsm.state import StatesGroup, State

class SetPreferenceStates(StatesGroup):
    waiting_for_country = State()
    waiting_for_city = State()
    waiting_for_title = State()
    waiting_for_company = State()
    waiting_for_min_salary = State()
    waiting_for_max_salary = State()
    confirming = State()

class EditPreferenceStates(StatesGroup):
    confirming = State()