from bot import bot
from telebot import types
from models import Homework, CompletedHomework, User
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Сообщение всем ученикам"))
def broadcast(message):
    bot.send_message(message.chat.id, "Введите сообщение")
    bot.register_next_step_handler(message, send)

def send(message):
    msg_text = message.text
    for student in message.current_group.users:
        if not student.is_student(message.current_group):
            continue
        bot.send_message(student.telegram_id, msg_text)

    bot.send_message(message.chat.id, "Сообщение отправлено!")
