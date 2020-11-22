from bot import bot
from telebot import types
from models import Homework, Group, CompletedHomework, User
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback
from scenarios.main_menu import send_main_menu


@bot.message_handler(func=callback("Посмотреть баллы"))
def get_marks(message):
    chat_id = message.chat.id
    user = User.from_telegram_id(chat_id)
    completed_homeworks = user.completed_homeworks

    s = ''
    for hw in completed_homeworks:
        if hw.is_checked():
            s += f'Дз {hw.id}, оценка: {hw.marks}'

            if hw.has_comment():
                s += f', комментарий: {hw.comment}'

            s += '\n'
        else:
            s += f'Дз {hw.id}, не проверено\n'
    bot.send_message(chat_id, s)
    send_main_menu(message)
