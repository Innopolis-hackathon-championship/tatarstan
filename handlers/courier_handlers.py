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


class DeliverFood(StatesGroup):
    looking_deliveries = State()
    writing_code_word = State()


db = DataBase()

router = Router()


@router.message(Command("my_deliveries"))
async def delivers(message: types.Message, state: FSMContext):
    deliver_builder = ReplyKeyboardBuilder()
    for deliver in db.get_delivers_from_user(message.from_user.id):  # get_delivers_from_user - функция для получения id пользователей кому должен доставить user
        deliver_builder.add(types.KeyboardButton(text=str(deliver['id'])))
    print(db.get_delivers_from_user(message.from_user.id))
    deliver_builder.adjust(3)

    await message.answer("Выберите id заказа для просмотра информации о заказе",
                         reply_markup=deliver_builder.as_markup(resize_keyboard=True,
                                                                input_field_placeholder="Выберите id заказа"))
    await state.set_state(DeliverFood.looking_deliveries)


@router.message(StateFilter(DeliverFood.writing_code_word),
                Command("cancel"))
async def back_from_code_word(message: types.Message, state: FSMContext):
    await delivers(message)

    await state.clear()


@router.message(DeliverFood.writing_code_word,
                F.text)
async def check_code_word(message: types.Message, state: FSMContext):
    id_from_state = await state.get_data()
    right_word = db.get_code_word_courier(id_from_state['courier_id'])

    if right_word == message.text:
        db.remove_order_in_couriers(id_from_state['courier_id'])

        deliver_builder = ReplyKeyboardBuilder()
        for deliver in db.get_delivers_from_user(
                message.from_user.id):  # db.get_delivers_from_user (db - база данных;
            # get_delivers_from_user - функция для получения id пользователей кому должен доставить user)
            deliver_builder.add(
                types.KeyboardButton(text=str(deliver['id'])))

        deliver_builder.adjust(3)

        await message.answer("Отилчно!\nСпасибо за доставку :)\n\nВыберите новую доставку, если такой нет, то отдыхайте)",
                             reply_markup=deliver_builder.as_markup(resize_keyboard=True,
                                                                    input_field_placeholder="Выберите id заказа"))
        await state.clear()
        await state.set_state(DeliverFood.looking_deliveries)
    else:
        await message.answer(
            "Кодовое слово не совпадает.\nПожалуйста, введи верное кодовое слово или вернитесь командой /cancel")


@router.message(F.text, StateFilter(DeliverFood.looking_deliveries))
async def check_order_by_userid(message: types.Message, state: FSMContext):
    if message.text in [str(i['id']) for i in db.get_delivers_from_user(message.from_user.id)]:
        user_info = None
        for i in db.get_delivers_from_user(message.from_user.id):
            if str(i['id']) == message.text:
                user_info = i
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Доставил",
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

        await message.answer("Такого заказа нет!\n"
                             "Выберите другой заказ из списка:",
                             reply_markup=deliver_builder.as_markup(resize_keyboard=True,
                                                                    input_field_placeholder="Выберите id пользователя"))


@router.callback_query(F.data.split(' ')[0] == "delivered")
async def check_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите кодовое слово:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(DeliverFood.writing_code_word)
    await state.update_data(courier_id=callback.data.split(' ')[1])


@router.callback_query(F.data.split(' ')[0] == "accept_order")
async def give_order_to_courier(callback: types.CallbackQuery):
    params = callback.data.split(' ')  # 0-accept_order(текст) 1-order_id 2-to_whom_id 3-name_of_to_whom 4-office 5-code_word
    db.set_courier(callback.message.chat.id, int(params[2]), params[3], params[4], params[5])
    db.del_order(int(params[1]))
    await callback.answer()
    await callback.message.edit_text("Для просмотра имеющихся заказов используйте команду /my_deliveries")



