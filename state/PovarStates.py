from aiogram.fsm.state import default_state, State, StatesGroup


class PovarState(StatesGroup):
    add_product_st = State()