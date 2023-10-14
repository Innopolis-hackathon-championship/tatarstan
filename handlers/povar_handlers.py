from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
import requests as rq
from config_data.config import Config, load_config
import random

config: Config = load_config('.env')

from state.PovarStates import PovarState
from database.DataBaseController import DataBase

from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon import LEXICON_RU
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state
from keyboards.povar_keyboards import orders_buttons, done_order_button, list_order_button, new_courier_button

# Инициализируем роутер уровня модуля
router = Router()
db = DataBase()


@router.message(Command('add_product'))
async def new_product(message: Message, state: FSMContext):
    user_data = db.get_user(message.from_user.id)
    if user_data['role'] == 1:
        await message.answer(
            "Введите название и количество товара\n в формате(название, количестов)\n\n"
            "Пример: Булочка с маком, 10")
        await state.set_state(PovarState.add_product_st)
    else:
        await message.answer(
            "У вас нет прав на использование этой команды")

@router.message(StateFilter(PovarState.add_product_st))
async def new_product2(message: Message, state: FSMContext):
    product_data = message.text.split(', ')
    await state.clear()
    if db.check_food_have(product_data[0]):
        db.update_food(product_data[0], int(product_data[1]))
    else:
        db.set_food(product_data[0], int(product_data[1]))
    product_data_base = db.get_food_amount(product_data[0])
    await message.answer(f"Количество товара успешно обновлено!\n"
                         f"Новое количество продукта: {product_data_base}")



async def code_word():
    possible_keys = "12345678990"
    return ''.join([random.choice(possible_keys) for _ in range(5)])


@router.message(Command('my_orders'))
async def my_orders(message: Message):
    user_data = db.get_user(message.from_user.id)
    if user_data['role'] == 1:
        print(any(orders_buttons().keyboard))
        if any(orders_buttons().keyboard):
            await message.answer(text="Несобранные заказы👇", reply_markup=orders_buttons(),
                                 disable_notification=False)
        else:
            await message.answer(text="Несобранные заказы👇", reply_markup=ReplyKeyboardRemove(),
                                 disable_notification=False)
    else:
        await message.answer(
            "У вас нет прав на использование этой команды❌")


@router.message(F.text[:4] == "ord:")
async def order_information(message: Message, state: FSMContext):
    order_data = db.get_order(message.text[4:])
    await message.answer(text="Загружаем выбранный заказ👇", reply_markup=ReplyKeyboardRemove())
    await message.answer(text=f"Номер заказа: {order_data['to_whom_id']}\n"
                              f"Заказ: {order_data['composition']}", reply_markup=done_order_button)
    await state.update_data(order_number=message.text[4:])
    await state.update_data(order_name=db.get_info_from_auth_keys(order_data['to_whom_id'])['name'])


@router.callback_query(F.data == '✅ Заказ готов')
async def order_done(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Спасибо, заказ будет передан курьеру", reply_markup=list_order_button)
    order_num = await state.get_data()
    order_data = db.get_order(order_num['order_number'])
    print(order_data)
    message_text = f"Новый заказ: {order_data['id']}"
    url = f'https://api.telegram.org/bot{config.tg_bot.token}/sendMessage'
    keyboard = {
        'inline_keyboard': [
            [
                {'text': '✅ Принять заказ',
                 'callback_data': f"a {order_data['id']} {order_data['to_whom_id']} {'_'.join((order_num['order_name'].split(' ')))} {order_data['office']} {await code_word()}"},
            ],
        ]
    }
    for i in db.get_all_couriers():
        message_data = {
            'chat_id': i,
            'text': message_text,
            'reply_markup': keyboard,
        }

        rq.post(url, json=message_data)


@router.callback_query(F.data == '⬅️ Назад')
@router.callback_query(F.data == "📋 Открыть список заказов")
async def my_orders_call(callback: CallbackQuery):
    if any(orders_buttons().keyboard):
        await callback.message.answer(text="Несобранные заказы👇", reply_markup=orders_buttons(),
                                      disable_notification=False)
    else:
        await callback.message.answer(text="Несобранные заказы👇", reply_markup=ReplyKeyboardRemove(),
                                      disable_notification=False)
