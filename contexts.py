from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMMenu(StatesGroup):
    start = State()

    user_panel = State()
    keywords = State()
    channels = State()
    chats = State()

    parse = State()


class FSMUserPanelActions(StatesGroup):
    add = State()
    watch = State()
    remove = State()

