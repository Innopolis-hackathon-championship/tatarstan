import asyncio
# import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from database.DataBaseController import DataBase
from aiogram.filters import StateFilter
from config_data.config import Config, load_config
import random
import requests as rq

config: Config = load_config('.env')


class DeliverFood(StatesGroup):
    looking_deliveries = State()
    writing_code_word = State()


db = DataBase()

router = Router()


@router.message(Command("my_deliveries"))
async def delivers(message: types.Message, state: FSMContext):
    if db.get_delivers_from_user(message.from_user.id):
        deliver_builder = ReplyKeyboardBuilder()
        for deliver in db.get_delivers_from_user(message.from_user.id):  # get_delivers_from_user - функция для получения id пользователей кому должен доставить user
            deliver_builder.add(types.KeyboardButton(text=str(deliver['id'])))
        print(db.get_delivers_from_user(message.from_user.id))
        deliver_builder.adjust(3)

        await message.answer("Выберите id заказа для просмотра информации о заказе 👇",
                         reply_markup=deliver_builder.as_markup(resize_keyboard=True,
                                                                input_field_placeholder="Выберите id заказа"))
        await state.set_state(DeliverFood.looking_deliveries)
    else:
        await message.answer("У вас нет заказов в данный момент, отдыхайте 😉")


@router.message(StateFilter(DeliverFood.writing_code_word),
                Command("cancel"))
async def back_from_code_word(message: types.Message, state: FSMContext):
    await state.clear()
    await delivers(message, state)


@router.message(DeliverFood.writing_code_word,
                F.text)
async def check_code_word(message: types.Message, state: FSMContext):
    id_from_state = await state.get_data()
    right_word = db.get_code_word_courier(id_from_state['courier_id'])
    if right_word == message.text:
        db.remove_order_in_couriers(id_from_state['courier_id'])

        deliver_builder = ReplyKeyboardBuilder()
        for deliver in db.get_delivers_from_user(message.from_user.id):  # db.get_delivers_from_user (db - база данных;
            # get_delivers_from_user - функция для получения id пользователей кому должен доставить user)
            deliver_builder.add(types.KeyboardButton(text=str(deliver['id'])))

        deliver_builder.adjust(3)

        await message.answer(
            "Отлично!\nСпасибо за доставку🙏\n\nВыберите новую доставку, если такой нет, то отдыхайте 😉",
            reply_markup=deliver_builder.as_markup(resize_keyboard=True,
                                                   input_field_placeholder="Выберите id заказа"))
        url = f'https://api.telegram.org/bot{config.tg_bot.token}/sendMessage'
        message_data = {
            'chat_id': id_from_state['user_id'],
            'text': "Спасибо за заказ 😊 Нам очень важно ваше мнение, оставьте пожалуйста отзыв. Это можно сдлеать по синей кнопке слева от клавиатуры"
        }
        rq.post(url, json=message_data)

        await state.clear()
        await state.set_state(DeliverFood.looking_deliveries)
    else:
        await message.answer(
            "Кодовое слово не совпадает.❌\nПожалуйста, введи верное кодовое слово или вернитесь командой /cancel")


@router.message(F.text, StateFilter(DeliverFood.looking_deliveries))
async def check_order_by_userid(message: types.Message, state: FSMContext):
    if message.text in [str(i['id']) for i in db.get_delivers_from_user(message.from_user.id)]:
        user_info = None
        for i in db.get_delivers_from_user(message.from_user.id):
            if str(i['id']) == message.text:
                user_info = i
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅ Доставил",
            callback_data=f"delivered {user_info['id']}"
        ))
        await message.reply("Информация о заказе:\n\n"
                            f"Кому доставлять: {user_info['name_of_to_whom']}\n"
                            f"Кабинет доставки: {user_info['office']}", reply_markup=builder.as_markup())
        await state.clear()
    else:
        deliver_builder = ReplyKeyboardBuilder()
        for deliver in db.get_delivers_from_user(
                message.from_user.id):  # db.get_delivers_from_user (db-база данных; get_delivers_from_user-функция)
            deliver_builder.add(
                types.KeyboardButton(text=str(deliver['id'])))  # допустим, deliver[0] - user_id кому доставлять

        deliver_builder.adjust(3)

        await message.answer("Такого заказа нет!\nЧтобы вывести список заказов используйте командку /my_deliveries")
        await state.clear()


@router.callback_query(F.data.split(' ')[0] == "delivered")
async def check_callback(callback: types.CallbackQuery, state: FSMContext):
    url = f'https://api.telegram.org/bot{config.tg_bot.token}/sendMessage'
    message_text = "Код подтваерждения: " + db.get_code_word_courier(callback.data.split(' ')[1])
    courier_info = db.get_courier_by_codeword(db.get_code_word_courier(callback.data.split(' ')[1]))
    if courier_info:
        message_data = {
            'chat_id': courier_info['to_whom_id'],
            'text': message_text
        }
        rq.post(url, json=message_data)
        await callback.message.answer("Введите код подтверждения:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(DeliverFood.writing_code_word)
        await state.update_data(courier_id=callback.data.split(' ')[1])
        await state.update_data(user_id=courier_info['to_whom_id'])
    else:
        await callback.message.answer("Вы уже доставляли этот заказ! ✅\nПосмотреть список заказов - /my_deliveries", reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data.split(' ')[0] == "a")
async def give_order_to_courier(callback: types.CallbackQuery):
    params = callback.data.split(' ')  # 0-a(текст) 1-order_id 2-to_whom_id 3-name_of_to_whom 4-office 5-code_word
    print(db.check_courier_order_id(params[1]), params[1])
    if db.check_courier_order_id(params[1]):
        db.set_courier(params[1], callback.message.chat.id, int(params[2]), params[3], params[4], params[5])
        db.del_order(int(params[1]))
        await callback.answer()
        await callback.message.edit_text("Для просмотра имеющихся заказов используйте команду /my_deliveries")
    else:
        await callback.message.edit_text("Этот заказ уже забрал другой курьер!")
