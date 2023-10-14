import asyncio
import logging
import random
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from database.DataBaseController import DataBase

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6405945930:AAES44ckOYx6HSjy68s9G29sAE5JXzjm1zA")
# Диспетчер
dp = Dispatcher()

db = DataBase()


def auth_key():
    possible_keys = "QWERTYUIOPASDFGHJKLZXCVBNM12345678990qwertyuiopasdfghjklzxcvbnm!_-/|"
    return ''.join([random.choice(possible_keys) for _ in range(8)])


# Хэндлер на команду /start

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    db.set_auth_key(message.from_user.id, message.from_user.full_name, auth_key())
    await message.answer("Спазибо за регистрацию в системе Столовая.bot")


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
