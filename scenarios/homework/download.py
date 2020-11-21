from bot import bot
from telebot import types
from models import Homework
from db import session

from filters import callback

@bot.message_handler(func=callback("Скачать домашнее задание"))
def add_homework(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Загрузите файл с ДЗ')
    bot.register_next_step_handler(msg, upload_homework)