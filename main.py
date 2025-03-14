import io
import os
import time
from typing import final

import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile, BufferedInputFile
from dotenv import load_dotenv

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from base64 import b64decode
from datetime import datetime
from io import BytesIO

from PIL import Image

load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=bot_token)

def first_kb():
    kb_list = [
        [KeyboardButton(text="1"), KeyboardButton(text="2"),
         KeyboardButton(text="3"), KeyboardButton(text="4")],
         [KeyboardButton(text="5"), KeyboardButton(text="6"),
         KeyboardButton(text="7"), KeyboardButton(text="8")],
         [KeyboardButton(text="9"), KeyboardButton(text="10"),
         KeyboardButton(text="11")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def second_kb():
    kb_list = [
        [KeyboardButton(text="РАС (Расстройство аутистического спектра)")], [KeyboardButton(text="ЗПР (Задержка психического развития)")],[KeyboardButton(text="Синдром Дауна")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def third_kb():
    kb_list = [
        [KeyboardButton(text="Составить тест по теме")], [KeyboardButton(text="Облегчить понимание материала для ученика")], [KeyboardButton(text="Изменить данные ученика")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def fourth_kb():
    kb_list = [
        [KeyboardButton(text="Химия"), KeyboardButton(text="Математика"), KeyboardButton(text="Русский язык")],
        [KeyboardButton(text="Биология"), KeyboardButton(text="Информатика"), KeyboardButton(text="Физика")],
        [KeyboardButton(text="Обществознание"), KeyboardButton(text="География"), KeyboardButton(text="История")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard



load_dotenv()
folder_id = os.getenv("YANDEX_FOLDER_ID")
api_key = os.getenv("YANDEX_API_KEY")
gpt_model = 'yandexgpt-lite'

class UserInfo(StatesGroup):
    user_name = State()
    clas = State()
    disability = State()
    type = State()
    predmet = State()
    material = State()
    tema = State()
    cnt = State()

async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(UserInfo.user_name)
    await bot.send_photo(photo=FSInputFile('ava.jpeg'), chat_id=message.from_user.id, caption="Привет!\nМы команда БИнарния представляем нашу онлайн платформу Together we learn (TWL).\nНаша миссия: решение остро-социальной проблемы инклюзивного образования.\nПлатформа предлагает помощь учителям по подготовке материалов для проведения уроков в классах с детьми с ООП.\n\n\nПожалуйста, напишите имя ученика:")

async def user_name(message: Message, state: FSMContext) -> None:
    data = await state.update_data(user_name=message.text)
    await state.set_state(UserInfo.clas)
    await message.answer("Теперь выберите класс ученика:", reply_markup=first_kb())

async def clas(message: Message, state: FSMContext) -> None:
    data = await state.update_data(clas=message.text)
    if data['clas'] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
        await state.set_state(UserInfo.clas)
        await message.answer("Пожалуйста, выберите класс ученика из списка:", reply_markup=first_kb())
    else:
        await state.set_state(UserInfo.disability)
        await message.answer("Отлично! Теперь выберите проблему вашего ученика:", reply_markup=second_kb())

async def disability(message: Message, state: FSMContext) -> None:
    data = await state.update_data(disability=message.text)
    if data['disability'] not in ['РАС (Расстройство аутистического спектра)', 'ЗПР (Задержка психического развития)', 'Синдром Дауна']:
        await state.set_state(UserInfo.disability)
        await message.answer("Пожалуйста, выберите проблему ученика из списка:", reply_markup=second_kb())
    else:
        await state.set_state(UserInfo.type)
        await message.answer("Понятно, мы постараемся Вам помочь! Выберите тип задачи:", reply_markup=third_kb())

async def task(message: Message, state: FSMContext) -> None:
    data = await state.update_data(type=message.text)
    if data['type'] not in ['Составить тест по теме', 'Облегчить понимание материала для ученика', 'Изменить данные ученика']:
        await state.set_state(UserInfo.type)
        await message.answer("Пожалуйста, выберите тип задачи из списка:", reply_markup=third_kb())
    else:
        if data['type'] == 'Составить тест по теме':
            await state.set_state(UserInfo.predmet)
            await message.answer("Хорошо! По какому предмету нужно составить тест?", reply_markup=fourth_kb())
        elif data['type'] == 'Облегчить понимание материала для ученика':
            await state.set_state(UserInfo.material)
            await message.answer("Хорошо! Отправьте текст, который Вы хотели бы сделать более понятным для ученика:")
        else:
            await state.set_state(UserInfo.user_name)
            await message.answer("Хорошо! Пожалуйста, напишите имя ученика:")

async def tema(message: Message, state: FSMContext) -> None:
    data = await state.update_data(predmet=message.text)
    await state.set_state(UserInfo.tema)
    await message.answer("Принято! По какой теме нужно сделать тест?")

async def cnt(message: Message, state: FSMContext) -> None:
    data = await state.update_data(tema=message.text)
    await state.set_state(UserInfo.cnt)
    await message.answer("Хорошо, сколько вопросов должно быть в тесте?")


async def test(message: Message, state: FSMContext) -> None:
    await message.answer("Подождите несколько секунд...")
    dataa = await state.update_data(cnt=message.text)
    user_prompt = f"Сделай тест по предмету: {dataa['predmet']}, по теме: {dataa['tema']}, для ученика из {dataa['clas']} класса, с количеством вопросов: {dataa['cnt']}, обязательно учитывая заболевание ученика: {dataa['disability']}. Отправь только тему теста и сам тест"
    print(user_prompt)
    body = {
        'modelUri': f'gpt://{folder_id}/{gpt_model}',
        'completionOptions': {'stream': False, 'temperature': 0.3, 'maxTokens': 2000},
        'messages': [
            {'role': 'user', 'text': user_prompt},
        ],
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(url, headers=headers, json=body)

    operation_id = response.json().get('id')

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        time.sleep(2)

    data = response.json()
    final_text = data['response']['alternatives'][0]['message']['text']
    print(data['response'])
    await message.answer(final_text.replace('*', ''))
    await state.set_state(UserInfo.type)
    await message.answer("Готово! С чем еще мы можем помочь?", reply_markup=third_kb())

async def text(message: Message, state: FSMContext) -> None:
    await message.answer("Подождите несколько секунд...")
    dataa = await state.update_data(material=message.text)
    user_prompt = f"Переделай данный текст так, чтобы он стал наиболее понятен ученику с Аутизмом:\n{dataa['material']}"
    body = {
        'modelUri': f'gpt://{folder_id}/{gpt_model}',
        'completionOptions': {'stream': False, 'temperature': 0.3, 'maxTokens': 2000},
        'messages': [
            {'role': 'user', 'text': user_prompt},
        ],
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(url, headers=headers, json=body)

    operation_id = response.json().get('id')

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        time.sleep(2)

    data = response.json()
    final_text = data['response']['alternatives'][0]['message']['text']
    await message.answer(final_text.replace('*', ''))
    await state.set_state(UserInfo.type)
    await message.answer("Готово! С чем еще мы можем помочь?", reply_markup=third_kb())



async def main() -> None:

    dp = Dispatcher()
    dp.message.register(start, Command("start"))
    dp.message.register(user_name, UserInfo.user_name)
    dp.message.register(clas, UserInfo.clas)
    dp.message.register(disability, UserInfo.disability)
    dp.message.register(task, UserInfo.type)
    dp.message.register(tema, UserInfo.predmet)
    dp.message.register(cnt, UserInfo.tema)
    dp.message.register(test, UserInfo.cnt)
    dp.message.register(text, UserInfo.material)


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
