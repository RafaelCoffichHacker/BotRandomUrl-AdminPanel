from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,  ReplyKeyboardRemove


def button():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("⚙️Useless Information")
    btn1 = KeyboardButton("🐈Get the photo of a cat")
    btn2 = KeyboardButton("😂Get random joke")
    btn3 = KeyboardButton("🥸🧾Get random user")
    button.row(btn, btn1)
    button.row(btn2, btn3)
    return button

def button1():
    button1 = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("⚙️Useless Information")
    btn11 = KeyboardButton("🐈Get the photo of a cat")
    btn21 = KeyboardButton("😂Get random joke")
    btn31 = KeyboardButton("🥸🧾Get random user")
    btn51 = KeyboardButton("🗄️📜Bot's statistic")
    btn61 = KeyboardButton("👤⚡🪫Active users")
    btn99 = KeyboardButton("🔗Forward to everyone")
    button1.row(btn99)
    button1.row(btn51, btn61)
    button1.row(btn1, btn11)
    button1.row(btn21, btn31)
    return button1

