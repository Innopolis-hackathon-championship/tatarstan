from aiogram.fsm.state import default_state, State, StatesGroup


class AdminState(StatesGroup):
    increase_balance = State()
    set_role = State()