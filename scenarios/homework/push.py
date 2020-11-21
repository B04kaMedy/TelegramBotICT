from bot import bot
from telebot import types
from models import Homework, Group, CompletedHomework, User
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Сдать домашнее задание"))
def push_homework(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for hw in message.current_group.homeworks:
        markup.add(KeyboardButton(hw.id))

    bot.send_message(chat_id, "Выберите ДЗ:", reply_markup=markup)

    bot.register_next_step_handler(message, push_next)

states = dict()

def push_next(message):
    states[message.chat.id] = message.text

    bot.send_message(message.chat.id, "Отправьте файл с домашкой")
    bot.register_next_step_handler(message, push_next2)

def push_next2(message):
    user = User.from_telegram_id(message.chat.id)
    chat_id = message.chat.id

    homework = session.query(Homework).get(states[message.chat.id])
    completed = CompletedHomework(
        homework=homework,
        file_telegram_id=message.document.file_id,
        student=user
    )

    bot.send_message(chat_id, "Файл загружен!")

    send_main_menu(message)
