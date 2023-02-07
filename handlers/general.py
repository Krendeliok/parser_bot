from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards import start_keyboard

from contexts import FSMMenu


async def start_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMMenu.start)
    await message.answer("Вітаю у боті для парсингу.", reply_markup=start_keyboard())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'], state="*")
