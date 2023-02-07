from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from contexts import FSMMenu, FSMUserPanelActions

from aiogram.dispatcher.filters import Text
from keyboards import user_panel_keyboard, user_panel_actions_keyboard, remove_keyboard

from commands import basic, user_panel, user_panel_actions, special
from utils import get_from_context, parse_text

from .general import start_command


async def user_panel_command(message: types.Message, state: FSMContext, **kwargs):
    await state.set_state(FSMMenu.user_panel)
    await message.reply("Меню користувача. Оберіть пункт.", reply_markup=user_panel_keyboard())


def back_handler(back_func):
    def wrapper(func):
        async def inner(message: types.Message, state: FSMContext, *args, **kwargs):
            if message.text == special["back"]:
                await back_func(message, state)
                return
            await func(message, state)
        return inner
    return wrapper


# ******************************************************************************************** User panel commands
@back_handler(start_command)
async def key_words_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMMenu.keywords)
    keywords = await get_from_context(state, "keywords")
    if keywords:
        text = f"Ваші ключові слова.\n{' '.join(keywords)}"
    else:
        text = "Ви ще не додавали ключові слова"
    await message.reply(
        text,
        reply_markup=user_panel_actions_keyboard()
    )


@back_handler(start_command)
async def channels_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMMenu.channels)
    channels = await get_from_context(state, "channels")
    if channels:
        text = f"Ваші канали.\n{' '.join(channels)}"
    else:
        text = "Ви ще не додавали канали"
    await message.reply(
        text,
        reply_markup=user_panel_actions_keyboard()
    )


@back_handler(start_command)
async def chats_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMMenu.chats)
    chats = await get_from_context(state, "chats")
    if chats:
        text = f"Ваші чати.\n{' '.join(chats)}"
    else:
        text = "Ви ще не додавали чати"
    await message.reply(
        text,
        reply_markup=user_panel_actions_keyboard()
    )


# ******************************************************************************************** Actions
@back_handler(user_panel_command)
async def add_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await state.set_state(FSMUserPanelActions.add)
    async with state.proxy() as data:
        data["state"] = current_state
    if current_state == FSMMenu.keywords.state:
        await message.reply("Напишіть ключові слова через пробіл, які хочете додати.", reply_markup=remove_keyboard())
    elif current_state == FSMMenu.channels.state:
        await message.reply("Напишіть посилання на канали через пробіл, які хочете додати.", reply_markup=remove_keyboard())
    elif current_state == FSMMenu.chats.state:
        await message.reply("Напишіть посилання на чати через пробіл, які хочете додати.", reply_markup=remove_keyboard())


async def add_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_state = data["state"]
        module = str(current_state).split(":")[1]
        module_data = data.get(module, set())
        for item in parse_text(message.text):
            module_data.add(item)
        data[module] = module_data

    await state.set_state(current_state)
    await message.answer("Додано успішно", reply_markup=user_panel_actions_keyboard())


@back_handler(user_panel_command)
async def remove_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await state.set_state(FSMUserPanelActions.remove)
    async with state.proxy() as data:
        data["state"] = current_state
    if current_state == FSMMenu.keywords.state:
        await message.reply("Напишіть ключові слова через пробіл, які хочете видалити.", reply_markup=remove_keyboard())
    elif current_state == FSMMenu.channels.state:
        await message.reply("Напишіть посилання на канали через пробіл, які хочете видалити.", reply_markup=remove_keyboard())
    elif current_state == FSMMenu.chats.state:
        await message.reply("Напишіть посилання на чати через пробіл, які хочете видалити.", reply_markup=remove_keyboard())


async def remove_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_state = data["state"]
        module = str(current_state).split(":")[1]
        module_data = data.get(module, set())
        for item in parse_text(message.text):
            try:
                module_data.remove(item)
            except KeyError:
                continue
        data[module] = module_data

    await state.set_state(current_state)
    await message.answer("Видалено успішно", reply_markup=user_panel_actions_keyboard())


# ******************************************************************************************** Register handlers
def register_actions(dp: Dispatcher, states_with_actions: list):
    for state in states_with_actions:
        dp.register_message_handler(
            add_command,
            Text(
                equals=[
                    str(i) for i in (user_panel_actions["add"], special["back"])
                ]
            ),
            state=state
        )
        dp.register_message_handler(
            remove_command,
            Text(equals=[
                    str(i) for i in (user_panel_actions["remove"], special["back"])
                ]
            ),
            state=state
        )


def register_handlers(dp: Dispatcher):
    states_with_actions = [
        FSMMenu.keywords,
        FSMMenu.channels,
        FSMMenu.chats,
    ]

    dp.register_message_handler(
        user_panel_command,
        Text(
            equals=[
                str(i) for i in (basic["user_panel"], special["back"])
            ]
        ),
        state=FSMMenu.start
    )
    dp.register_message_handler(
        key_words_command,
        Text(
            equals=[
                str(i) for i in (user_panel["keywords"], special["back"])
            ]
        ),
        state=FSMMenu.user_panel)
    dp.register_message_handler(
        channels_command,
        Text(
            equals=[
                str(i) for i in (user_panel["channels"], special["back"])
            ]
        ),
        state=FSMMenu.user_panel)
    dp.register_message_handler(
        chats_command,
        Text(
            equals=[
                str(i) for i in (user_panel["chats"], special["back"])
            ]
        ),
        state=FSMMenu.user_panel
    )

    register_actions(dp, states_with_actions)

    dp.register_message_handler(add_handler, state=FSMUserPanelActions.add)
    dp.register_message_handler(remove_handler, state=FSMUserPanelActions.remove)

