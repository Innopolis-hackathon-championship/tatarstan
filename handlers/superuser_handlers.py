from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from state.UserStates import UserState

import state.UserStates
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state
from database.DataBaseController import DataBase
from state.AdminStates import AdminState

# Инициализируем роутер уровня модуля
router: Router = Router()

db = DataBase()


@router.message(Command('add_balance'))
async def add_balance(message: Message, state: FSMContext):
    user_data = db.get_user(message.from_user.id)
    if user_data['role'] == 3:
        await message.answer("Для увеличения баланса пользователя введите через пробел: user_id, balance_chages")
        await state.set_state(AdminState.increase_balance)


@router.message(F.text, StateFilter(AdminState.increase_balance))
async def add_balance_end(message: Message, state: FSMContext):
    changes_data = message.text.split(' ')
    try:
        db.update_balance(changes_data[0], changes_data[1])
        await state.clear()
        await message.answer("Баланс пользователя успешно изменен")
    except:
        await message.answer("Такой пользователь не зарегестрирован")


@router.message(Command('set_role'))
async def set_role(message: Message, state: FSMContext):
    user_data = db.get_user(message.from_user.id)
    if user_data['role'] == 3:
        await message.answer(
            "Для изменения роли пользователя введите через пробел: user_id, role\n\n0 - обычный пользователь, 1 - курьуер, 2 - работник столовой")
        await state.set_state(AdminState.set_role)


@router.message(F.text, StateFilter(AdminState.set_role))
async def set_role_end(message: Message, state: FSMContext):
    changes_data = message.text.split(' ')
    try:
        db.set_user_role(changes_data[0], changes_data[1])
        await state.clear()
        await message.answer("Роль пользователя успешно изменена")
    except:
        await message.answer("Такой пользователь не зарегестрирован")
# Этот хэндлер срабатывает на команду /start


# Этот хэндлер срабатывает на команду /help
