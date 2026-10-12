import json
import time
import sqlite3
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import requests
from aiogram.dispatcher import FSMContext  # content type
from aiogram.dispatcher.filters.state import State, StatesGroup  # Для ячеек
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # create and registr in db cell

from config import *
from keyboard import button, button1

class AdminMessage(StatesGroup):
    msg = State()

storage = MemoryStorage()


bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def create_dp():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            full_name VARCHAR(50),
            username TEXT
        )
    """)
    connection.commit()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    if message.text == '/start':
        cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (user_id,))
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO users(telegram_id, full_name, username)
                VALUES (?, ?, ?)
            """, (user_id, full_name, username))
            connection.commit()
        if user_id not in ADMIN_IDS:
            await message.answer("Bot successfully activated!", reply_markup=button())
        else:
            await message.answer("Bot successfully activated!", reply_markup=button1())
    elif message.text == '/help':
        await message.answer("no one will help u")


@dp.message_handler(lambda msg: msg.text == "⚙️Useless Information")
async def handle_btns(message: Message):
    responde = requests.get(URL)
    data = responde.json()
    await message.answer(f"Here the information that you will never use: {data['text']}")


@dp.message_handler(lambda msg: msg.text == "🐈Get the photo of a cat")
async def handle(message: Message):
    responde = requests.get(CatURL)
    data = responde.json()
    await bot.send_photo(chat_id=message.chat.id, photo=data[0]['url'])


@dp.message_handler(lambda msg: msg.text == "😂Get random joke")
async def handle_joke(message: Message):
    responde = requests.get(JokeURL)
    data = responde.json()
    await message.answer(f"Here is the joke: {data['joke']}", reply_markup=button())


@dp.message_handler(lambda msg: msg.text == "🥸🧾Get random user")
async def handle_user(message: Message):
    responde = requests.get(random_user_URL)
    data = responde.json()
    user = data['results'][0]
    name = f"{user['name']['first']} {user['name']['last']}"
    email = user['email']
    username = user["login"]['username']
    password = user["login"]['password']
    street = f"{user['location']['street']['number']} {user['location']['street']['name']}"
    city = user['location']['city']
    country = user['location']['country']
    lat = float(user['location']['coordinates']['latitude'])
    lng = float(user['location']['coordinates']['longitude'])
    gender = user['gender']

    text = (
        f"Here is the information about random user:\n"
        f"name: {name}\n"
        f"gender: {gender}\n"
        f"email: {email}\n"
        f"username: {username}\n"
        f"password: <tg-spoiler>{password}</tg-spoiler>\n"
        f"country: {country}\n"
        f"street: {street}\n"
        f"Here is the location of this user"
    )

    await message.answer(text)
    await bot.send_location(chat_id=message.chat.id, latitude=lat, longitude=lng)

@dp.message_handler(lambda msg: msg.text == "🗄️📜Bot's statistic")
async def handle_statistic(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.answer(f"Not found")
    else:
        cursor.execute("SELECT COUNT(*) FROM users", )
        res = cursor.fetchone()
        await message.answer(f"The amount of people use this bot is {res[0]}")

@dp.message_handler(lambda msg: msg.text == "👤⚡🪫Active users")
async def \
        online_stat(message: Message):
    admin_id1 = message.from_user.id
    if admin_id1 not in ADMIN_IDS:
        cursor.execute("SELECT telegram_id FROM users")
        users = cursor.fetchall()
        print(users)
        count = 0
        for user in users:
            user_id = user[0]
            try:
                check = await bot.send_message(user_id, "Are you here?")
                print(check)
                await bot.delete_message(chat_id=user_id, message_id=check.message_id)
                count += 1
            except Exception as e:
               print(e)
            time.sleep(0.125)

        await message.answer(f"The amount of active users is {count}")
    else:
        await message.answer(f"Not found")


@dp.message_handler(lambda msg: msg.text == "🔗Forward to everyone")
async def resends(message: Message, state: FSMContext):
    admin_id1 = message.from_user.id
    if admin_id1 in ADMIN_IDS:
        await message.answer("send me the message")
        await AdminMessage.msg.set()
    else:
        await message.answer("Not found")


@dp.message_handler(state=AdminMessage.msg)
async def send_broadcast(message: Message, state: FSMContext):
    admin_id = message.from_user.id
    if admin_id in ADMIN_IDS:
        cursor.execute("SELECT telegram_id FROM users")
        users = cursor.fetchall()
        for user in users:
            user_id = user[0]
            await bot.copy_message(user_id, admin_id, message.message_id)
            time.sleep(0.125)
        await message.answer("successefuly done")
    await state.finish()


if __name__ == '__main__':
    create_dp()
    executor.start_polling(dp, skip_updates=True)