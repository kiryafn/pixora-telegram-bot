from aiogram.fsm.state import StatesGroup, State

class SetPreferenceStates(StatesGroup):
    """
    FSM states for the 'set preferences' flow:
      • waiting_for_country    – user selects a country
      • waiting_for_city       – user selects a city
      • waiting_for_title      – user enters a job title
      • waiting_for_company    – user selects or enters a company
      • waiting_for_min_salary – user enters minimum salary
      • waiting_for_max_salary – (optional) user enters maximum salary
      • confirming             – user confirms or cancels the setup
    """

    waiting_for_country = State()
    waiting_for_city = State()
    waiting_for_title = State()
    waiting_for_company = State()
    waiting_for_min_salary = State()
    waiting_for_max_salary = State()
    confirming = State()

class EditPreferenceStates(StatesGroup):
    """
    FSM state for editing an existing preference:
      • confirming – user confirms or cancels the edit
    """

    confirming = State()