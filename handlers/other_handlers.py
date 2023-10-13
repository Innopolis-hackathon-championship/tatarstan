from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from state.UserStates import UserState

import state.UserStates
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from database.utils import get_user, add_user
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state


# Инициализируем роутер уровня модуля
router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['start'])
    await state.set_state(UserState.auth)

@router.message(StateFilter(UserState.auth))
async def auth_user(message: Message, state: FSMContext):
    #create_user(id)
    user_data = await get_user(id)
    if ~(user_data['auth']):
        auth_key = message.text
        user_key = "AAAAAAAA"#get_user_key(message.from_user.id)['auth_key']
        if len(auth_key) != 8:
            await message.answer('Неверный формат ключа авторизации')
        else:
            if auth_key == user_key:
                await message.answer(f"Здравствуйте, {message.from_user.full_name},\nвы успешно авторизованы в нашем боте и\nможете использовать его функции,\nчтобы узнать функции, доступные для \nвас используйте команду /help")
                await state.clear()
            else:
                await message.answer('Неверный ключ авторизации')
    else:
        await message.answer('Вы уже авторизованы, чтобы\nузнать свои возможности напишите /help')
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user_data = await get_user(message.from_user.id)
    await message.answer(text=LEXICON_RU[f"/help{user_data['role']}"])
