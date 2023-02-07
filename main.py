import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

from c import create_client


API_TOKEN = config.BOT_TOKEN
API_ID = config.TELEGRAM_API_ID
API_HASH = config.TELEGRAM_API_HASH

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

phone = '+380955981713'

client = create_client(phone, API_ID, API_HASH)
client.start()


from handlers import general, user_panel, parse

general.register_handlers(dp)
user_panel.register_handlers(dp)
parse.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
