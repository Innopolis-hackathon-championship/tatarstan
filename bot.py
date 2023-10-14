import asyncio
import logging
from database.DataBaseController import DataBase
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers, povar_handlers, courier_handlers
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)
# Загружаем конфиг в переменную config
config: Config = load_config('.env')

# Инициализируем бот и диспетчер
bots: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)

# Регистриуем роутеры в диспетчере
dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)
dp.include_router(povar_handlers.router)
dp.include_router(courier_handlers.router)

db = DataBase()

# Функция конфигурирования и запуска бота
async def main():

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bots.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(main())