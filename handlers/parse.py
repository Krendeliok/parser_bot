import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from contexts import FSMMenu

from commands import basic

from keyboards import start_keyboard

from c import client

from mako.template import Template


def render_html_result(parsing_data):
    template = Template(filename=os.path.join(os.getcwd(), 'templates', 'main.html'))
    return template.render(parsing_data=parsing_data)


async def get_messages_by_keyword(chat_entity, keyword):
    return [
        (
            message,
            await client.get_entity(message.from_id if message.from_id else chat_entity.id)
        )
        for message in await client.iter_messages(chat_entity, search=keyword).collect()
    ]


async def get_all_messages_in_chat(chat_entity, keywords):
    return sum([await get_messages_by_keyword(chat_entity, keyword) for keyword in keywords], start=[])


async def parse(keywords, chats: set, channels: set):
    chats_entities = [await client.get_entity(chat_id) for chat_id in chats | channels]
    messages = {
        chat_entity.title: await get_all_messages_in_chat(chat_entity, keywords) for chat_entity in chats_entities
    }
    text = render_html_result(messages)
    with open(os.path.join(os.getcwd(), "tempfiles", "result.html"), "w") as f:
        f.write(text)


async def parse_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMMenu.parse)
    async with state.proxy() as data:
        keywords = data.get("keywords")
        keywords = ["парсинг", "парс"]
        if keywords is None:
            await message.answer("Немає жодного ключового слова, вкажіть його у панелі користувача", reply_markup=start_keyboard())
            await state.set_state(FSMMenu.start)
            return
        channels = data.get("channels", set())
        #channels = {"https://t.me/+UXBXiYj2WVAyOTc6"}
        chats = data.get("chats", set())
        #chats = {"https://t.me/+giKcLe6ZbY9jZGMy"}
    if any((chats, channels)):
        await message.answer("Почекайте, це може зайняти деякий час.")
        await parse(keywords, chats, channels)
        await message.answer_document(types.InputFile(os.path.join(os.getcwd(), "tempfiles", "result.html"), "result.html"))
    else:
        await message.answer("Вкажіть хоч один чат або канал у панель користувача", reply_markup=start_keyboard())
    await state.set_state(FSMMenu.start)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(parse_command, Text(equals=basic["start_parsing"]), state=FSMMenu.start)
