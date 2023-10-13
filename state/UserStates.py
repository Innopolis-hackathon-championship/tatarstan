from aiogram.fsm.state import default_state, State, StatesGroup


class UserState(StatesGroup):
    bet_page = State()
    auth= State()
