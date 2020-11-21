from bot import bot
from telebot import types
from models import Homework
from db import session
from filters import callback


# TODO    deadline

@bot.message_handler(func=callback("Добавить дз"))
def add_homework(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Загрузите файл с ДЗ')
    bot.register_next_step_handler(msg, upload_homework)


def upload_homework(message):
    chat_id = message.chat.id
    homework_id = message.document.file_id
    homework = Homework(file_telegram_id=homework_id, deadline="", group=message.current_group)
    session.add(homework)
    session.commit()
    bot.send_message(chat_id, "Файл загружен!")
