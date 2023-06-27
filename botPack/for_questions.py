from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram import Router

route = Router()


# HOST = "http://127.0.0.1:8000"
HOST = "http://host.docker.internal:8000"


def get_type_stanok() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Токарный")
    kb.button(text="Сверлильный")
    kb.button(text="Фрезерный")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def type_of_machine(callback: types.Message):
    callback = callback.text.lower()
    if callback == 'токарный':
        kb = ReplyKeyboardBuilder()
        kb.button(text="SPV-500C")
        kb.button(text="SPF-1500P")
        kb.button(text="Proma SM-300E")
        kb.button(text="CU400")
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

    elif callback == 'сверлильный':
        kb = ReplyKeyboardBuilder()
        kb.button(text="2с108п")
        kb.button(text="B1825G")
        kb.button(text="2М112")
        kb.button(text="ГС520")
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


    elif callback == 'фрезерный':
        kb = ReplyKeyboardBuilder()
        kb.button(text="X6142")
        kb.button(text="Optimum MT200")
        kb.adjust(1)
        return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

