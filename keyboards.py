from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from commands import basic, user_panel, user_panel_actions, special


def reply_keyboard(*, row_width=3, resize_keyboard=True):
    def wrapper(func):
        def inner(*args, **kwargs):
            keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
            func(keyboard, *args, **kwargs)
            return keyboard
        return inner
    return wrapper


def add_back_button(func):
    def wrapper(keyboard: ReplyKeyboardMarkup, *args, **kwargs):
        keyboard.add(KeyboardButton(special["back"]))
        func(keyboard, *args, **kwargs)
    return wrapper


@reply_keyboard()
def start_keyboard(keyboard: ReplyKeyboardMarkup):
    for key, value in basic.items():
        keyboard.insert(KeyboardButton(f"{value}"))


@reply_keyboard()
@add_back_button
def user_panel_keyboard(keyboard: ReplyKeyboardMarkup):
    for key, value in user_panel.items():
        keyboard.insert(KeyboardButton(f"{value}"))


@reply_keyboard()
@add_back_button
def user_panel_actions_keyboard(keyboard: ReplyKeyboardMarkup):
    for key, value in user_panel_actions.items():
        keyboard.insert(KeyboardButton(f"{value}"))


def remove_keyboard():
    return ReplyKeyboardRemove()
