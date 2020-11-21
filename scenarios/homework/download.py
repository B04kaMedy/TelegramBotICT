from bot import bot
from telebot import types
from models import Homework, Group
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback

@bot.message_handler(func=callback("Скачать домашнее задание"))
def add_homework(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for hw in message.current_group.homeworks:
        markup.add(KeyboardButton(hw.id))

    bot.send_message(chat_id, "Выберите ДЗ:", reply_markup=markup)

    bot.register_next_step_handler(message, upload_homework)

def upload_homework(message):
    chat_id = message.chat.id
    homework = session.query(Homework).get(message.text)

    bot.send_document(message.chat.id, homework.file_telegram_id)

    send_main_menu(message)