from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from state.UserStates import UserState

import state.UserStates
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from database.utils import get_user
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='menu'))
async def process_help_command(message: Message):



# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(F.text == 'profile')
@router.message(Command(commands='profile'))
async def process_profile_command(message: Message):
    user_data = get_user(message.from_user.id)
    await message.answer(text=f"🪪 ID: {user_data['user_id']}\n\n"
                                         f"👤 ФИО: {user_data['username'] if user_data['username'] else 'не заполнено'}\n\n"
                                         f"🏠 Адрес: {user_data['adress'] if user_data['adress'] else 'не заполнено'}\n\n"
                                         f"☎️ Номер телефона: {user_data['phone_number'] if user_data['phone_number'] else 'не заполнено'}\n\n"
                                         f"🛒 Всего покупок: {user_data['order_value']}\n\n"
                                         f"🔥 Персональная скидка: {user_data['personal_sale']}%\n\n"
                                         f"🗒 Примечания: {user_data['notes'] if user_data['notes'] else 'не заполнено'}")


