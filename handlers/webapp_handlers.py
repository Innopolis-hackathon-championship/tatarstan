from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from state.UserStates import UserState
from aiogram.enums.content_type import ContentType

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


def webAppKeyboard():  # создание клавиатуры с webapp кнопкой
    keyboard = ReplyKeyboardBuilder()  # создаем клавиатуру
    webAppTest = WebAppInfo(url="https://deldorenok.github.io/")  # создаем webappinfo - формат хранения url
    one_butt = KeyboardButton(text="📋 Меню буфета", web_app=webAppTest)  # создаем кнопку типа webapp
    keyboard.add(one_butt)  # добавляем кнопки в клавиатуру
    return keyboard.as_markup(resize_keyboard=True)


@router.message(Command('menu'))
async def menu(message: Message):
    await message.answer('Чтобы открыть меню, нажмите на кнопку под клавиатурой👇', reply_markup=webAppKeyboard())


@router.message(F.content_type == "web_app_data")  # получаем отправленные данные
async def answer(webAppMes):
    print(webAppMes)  # вся информация о сообщении
    print(webAppMes.chat.id)
    user_data = db.get_user(webAppMes.chat.id)
    order_dt = webAppMes.web_app_data.data.split(' ')
    pd_data = ["Беккен", "Сосиска в тесте", "Очпочмак", "Круассан", "Пицца"]
    for i in range(1, 6):
        if int(order_dt[i]) > db.get_food_amount(f'{pd_data[i - 1]}'):
            await webAppMes.answer(f"❌ Недостаточное количество продукта {pd_data[i-1]}")
            return
    if float(user_data['balance']) < float(order_dt[len(order_dt)-1]):
        await webAppMes.answer("❌ У вас недостаточно средств(")
    else:
        order_data = f"Беккен:{order_dt[1]}шт Сосиска в тесте:{order_dt[2]}шт Очпочмак:{order_dt[3]}шт Круассан:{order_dt[4]}шт Пицца:{order_dt[5]}шт"
        for i in range(1, 6):
            if int(order_dt[i]) <= db.get_food_amount(f'{pd_data[i - 1]}'):
                db.update_food(f'{pd_data[i - 1]}', order_dt[i]*-1)
        db.set_order(webAppMes.chat.id, '_'.join(db.get_info_from_auth_keys(webAppMes.chat.id)['name'].split(' ')), order_data, str(order_dt[0])) # конкретно то что мы передали в бота
        print(webAppMes.chat.id, '_'.join(db.get_info_from_auth_keys(webAppMes.chat.id)['name'].split(' ')), order_data, str(order_dt[0]))
        await webAppMes.answer("Спасибо за заказ😊, как только курьер будет готов его вам передать, вы получите код потдтверждения.")
        db.update_balance(webAppMes.chat.id, -float(order_dt[len(order_dt)-1]))


    # отправляем сообщение в ответ на отправку данных из веб-приложения

