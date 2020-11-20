from bot import bot
from telebot import types


@bot.callback_query_handler(func=lambda call: call.data == "add homework")
def add_homework(message):
    chat_id = message.chat.id
	msg = bot.send_message(chat_id, 'Загрузите файл с ДЗ')
    bot.register_next_step_handler(msg, upload_homework)

def upload_homework(message):
    chat_id = message.chat.id
    homework_id = message.document.file_id
    homework = Homework(task=homework_id, deadline=None)

    user.current_homework = homework

    create_homework(homework)
    msg = bot.send_message(chat_id, "Установите дедлайн (1.1.2020)")
    bot.register_next_step_handler(msg, set_deadline)

def set_deadline(message):
    chat_id = message.chat.id
    homework = user.current_homework
    homework.deadline = message.text
    #Ой да фпесду