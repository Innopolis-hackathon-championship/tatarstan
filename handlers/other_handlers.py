from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from state.UserStates import UserState

from database.DataBaseController import DataBase
import state.UserStates
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state

# Инициализируем роутер уровня модуля
router: Router = Router()
db = DataBase()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    try:
        if db.get_user(message.from_user.id)['auth']:
            await message.answer('Вы уже авторизованы, чтобы\nузнать свои возможности напишите /help')
            print("aut")
            return
    except:
        await message.answer(text=LEXICON_RU['start'])
        await state.set_state(UserState.auth)


@router.message(StateFilter(UserState.auth))
async def auth_user(message: Message, state: FSMContext):
    auth_key = message.text
    if len(auth_key) != 8:
        await message.answer('Неверный формат ключа авторизации')
    else:
        print(db.check_auth_key(message.from_user.id, auth_key))
        if db.check_auth_key(message.from_user.id, auth_key):
            db.set_user(user_id=message.from_user.id)
            db.set_user_auth(message.from_user.id)
            await message.answer(
                f"Здравствуйте, {message.from_user.full_name},\nвы успешно авторизованы в нашем боте и\nможете использовать его функции,\nчтобы узнать функции, доступные для \nвас используйте команду /help")
            await state.clear()
            return
        else:
            await message.answer('Неверный ключ авторизации')


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user_data = db.get_user(message.from_user.id)
    await message.answer(text=LEXICON_RU[f"/help{user_data['role']}"])
