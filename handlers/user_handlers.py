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
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user_data = get_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/help'])


