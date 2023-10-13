from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
import requests as rq
from config_data.config import Config, load_config

config: Config = load_config('.env')

from state.PovarStates import PovarState

from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from database.utils import get_user, add_user, add_product, get_order, set_order_state, get_all_couriers
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state
from keyboards.povar_keyboards import orders_buttons, done_order_button, list_order_button, new_courier_button

# Инициализируем роутер уровня модуля
router = Router()

'''
@router.message(Command('add_product'))
async def new_product(message: Message, state: FSMContext):
    user_data = await get_user(message.from_user.id)
    if user_data['role'] == 1:
        await message.answer(
            "Введите параметры нового товара\n в формате(название, количестов, цена в руб)\n\n"
            "Пример: Булочка с маком, 10, 100")
        await state.set_state(PovarState.add_product_st)
    else:
        await message.answer(
            "У вас нет прав на использование этой команды")

@router.message(StateFilter(PovarState.add_product_st))
async def new_product2(message: Message, state: FSMContext):
    product_data = message.text.split(', ', maxsplit=2)
    await state.clear()
    await add_product(product_data[0], product_data[1], product_data[2])
'''


@router.message(Command('my_orders'))
async def my_orders(message: Message):
    user_data = await get_user(message.from_user.id)
    if user_data['role'] == 1:
        await message.answer(text="Несобранные заказы", reply_markup=orders_buttons,
                             disable_notification=False)
    else:
        await message.answer(
            "У вас нет прав на использование этой команды")


@router.message(F.text[:4] == "ord:")
async def order_information(message: Message, state: FSMContext):
    order_data = await get_order(message.text[4:])
    print(message.text[4:])
    await message.answer(text=f"Номер заказа: {order_data['id']}\n"
                              f"Заказ: {order_data['composition']}", reply_markup=done_order_button)
    await state.update_data(order_number=message.text[4:])


@router.callback_query(F.data == '✅ Заказ готов')
async def order_done(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Спасибо, заказ будет передан курьеру", reply_markup=list_order_button)
    order_num = await state.get_data()
    await set_order_state(order_num, 1)
    message_text = f"Новый заказ: {order_num['order_number']}"
    url = f'https://api.telegram.org/bot{config.tg_bot.token}/sendMessage'
    keyboard = {
        'inline_keyboard': [
            [
                {'text': '✅ Принять заказ', 'callback_data': 'accept_order'},
            ],
        ]
    }
    for i in await get_all_couriers():
        message_data = {
            'chat_id': i,
            'text': message_text,
            'reply_markup': keyboard,
        }

        rq.post(url, json=message_data)


@router.callback_query(F.data == "📋 Открыть список заказов")
async def my_orders_call(callback: CallbackQuery):
    user_data = await get_user(callback.message.from_user.id)
    await callback.answer()
    if user_data['role'] == 1:
        await callback.message.answer(text="Несобранные заказы", reply_markup=orders_buttons,
                                      disable_notification=False)
    else:
        await callback.message.answer(
            "У вас нет прав на использование этой команды")
