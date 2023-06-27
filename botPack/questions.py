import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import requests
from aiogram.filters.state import StatesGroup, State
import json

from for_questions import (type_of_machine, get_type_stanok)


# HOST = "http://127.0.0.1:8000"
HOST = "http://host.docker.internal:8000"

router = Router()  # [1]


class Settings(StatesGroup):
    id_machine = int
    response_settings = {}
    message = State()
    list_settings = {}


class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_password = State()


class AuthState(StatesGroup):
    waiting_for_password = State()
    count = 3


@router.message(Command("start"))
async def any_message(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    response = requests.get(HOST + f'/api/users/{user_id}')

    if response.json():
        await message.answer(f'Здравствуйте, {response.json()["first_name"]}! Введите пароль:')
        await state.set_state(AuthState.waiting_for_password)
    else:
        await message.answer('Здравствуйте! Пожалуйста, введите имя.')
        await state.set_state(Registration.waiting_for_name)


@router.message(AuthState.waiting_for_password)
async def user_pass(message: types.Message, state: FSMContext):
    user_password = message.text
    user_id = message.chat.id
    response = requests.get(HOST + f"/api/auth?uid={user_id}&password={user_password}")
    count = AuthState.count
    count -= 1
    if response.json():
        await message.answer('Вход выполнен.\nВыберите тип станка', reply_markup=get_type_stanok())
        await state.clear()
    else:
        await message.answer('Неверный пароль. Попробуйте снова!')
        if count > 0:
            await message.answer(f'У вас осталось попыток: {count + 1}')
            AuthState.count = count
            await state.set_state(AuthState.waiting_for_password)
        else:
            await message.answer('Доступ запрещен')


@router.message(Registration.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    Registration.waiting_for_name = message.text.strip()
    await message.answer('Пожалуйста, введите фамилию.')
    await state.set_state(Registration.waiting_for_surname)


@router.message(Registration.waiting_for_surname)
async def get_surname(message: types.Message, state: FSMContext):
    Registration.waiting_for_surname = message.text.strip()
    await message.answer('Введите пароль')
    await state.set_state(Registration.waiting_for_password)


@router.message(Registration.waiting_for_password)
async def get_password(message: types.Message):
    user_last_name = Registration.waiting_for_surname
    user_name = Registration.waiting_for_name
    user_password = message.text.strip()
    user_id = message.chat.id
    response = requests.post(
        HOST + f"/api/users?firstname={user_name}&surname={user_last_name}&telegram_id={user_id}&password={user_password}")

    try:
        if response.json():
            await message.answer('Вход выполнен', reply_markup=get_type_stanok())
    except requests.JSONDecodeError:
        text = "*" * 50 + "\n" + response.text
        print(text)
        await message.answer("Ошибка при регистрации. Перезапустите бота!")


@router.message(Text(text=["Токарный", "Сверлильный", "Фрезерный"], ignore_case=True))
async def choose_model_stanok(message: Message):
    await message.answer(
        "Выберите модель станка",
        reply_markup=type_of_machine(message)
    )


@router.message(Settings.message)
async def set_machine(message: types.Message, state: FSMContext):
    settings = Settings.response_settings
    id_machine = Settings.id_machine

    if settings:
        await message.answer(f'Введите {settings[0]}')
        Settings.list_settings[settings[0]] = message.text
        del settings[0]
        Settings.response_settings = settings
        await state.set_state(Settings.message)
    else:
        data = {
            "uid": message.from_user.id,
            "settings": json.dumps(Settings.list_settings),
            "machine_id": id_machine,
            "datetime": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        data = json.dumps(data)
        requests.post(HOST + '/api/setting', data=data)
        await message.answer(f'Ваши настройки успешно сохранены.', reply_markup=get_type_stanok())


def post_settings(callback):
    response = requests.get(HOST + f'/api/machine?name={callback}')
    settings = json.loads(response.json()["settings"])
    id_machine = response.json()["id"]
    return settings, id_machine


@router.message(Text(text=["SPV-500C", "SPF-1500P", "Proma SM-300E", "CU400"], ignore_case=True))
async def tokarnii(message: Message, state: FSMContext):
    message_1 = message.text.upper()

    if message_1 == 'SPV-500C':
        Settings.response_settings, Settings.id_machine = post_settings("SPV-500C")
        await set_machine(message, state)
    elif message_1 == 'SPF-1500P':
        Settings.response_settings, Settings.id_machine = post_settings('SPF-1500P')
        await set_machine(message, state)
    elif message_1 == 'Proma SM-300E'.upper():
        Settings.response_settings, Settings.id_machine = post_settings('Proma SM-300E')
        await set_machine(message, state)
    elif message_1 == 'CU400':
        Settings.response_settings, Settings.id_machine = post_settings('CU400')
        await set_machine(message, state)


@router.message(Text(text=["2с108п", "B1825G", "2М112", "ГС520"], ignore_case=True))
async def sverlilnii(message: Message, state: FSMContext):
    message_1 = message.text.upper()

    if message_1 == '2с108п'.upper():
        Settings.response_settings, Settings.id_machine = post_settings("2с108п")
        await set_machine(message, state)
    elif message_1 == 'B1825G':
        Settings.response_settings, Settings.id_machine = post_settings('B1825G')
        await set_machine(message, state)
    elif message_1 == '2М112':
        Settings.response_settings, Settings.id_machine = post_settings('2М112')
        await set_machine(message, state)
    elif message_1 == 'ГС520':
        Settings.response_settings, Settings.id_machine = post_settings('ГС520')
        await set_machine(message, state)


@router.message(Text(text=["X6142", "Optimum MT200"], ignore_case=True))
async def frezernii(message: Message, state: FSMContext):
    message_1 = message.text.upper()

    if message_1 == 'X6142':
        Settings.response_settings, Settings.id_machine = post_settings('X6142')
        await set_machine(message, state)
    elif message_1 == 'Optimum MT200'.upper():
        Settings.response_settings, Settings.id_machine = post_settings('Optimum MT200')
        await set_machine(message, state)
