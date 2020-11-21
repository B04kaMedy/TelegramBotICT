from bot import bot
from telebot import types
from models import Homework, Group, CompletedHomework, User
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Проверить дз"))
def check_homework(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for hw in message.current_group.homeworks:
        markup.add(KeyboardButton(hw.id))

    bot.send_message(chat_id, "Выберите дз для проверки", reply_markup=markup)

    bot.register_next_step_handler(message, check_next)

states = dict()

def check_next(message):
    chat_id = message.chat.id
    homework = session.query(Homework).get(message.text)

    states[chat_id] = homework

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for completed_homework in homework.completed_homeworks:
        if completed_homework.is_checked():
            continue
        markup.add(KeyboardButton(completed_homework.student.name))
    
    bot.send_message(chat_id, "ВЫберите ученика", reply_markup=markup)
    bot.register_next_step_handler(message, check_next2)

def check_next2(message):
    chat_id = message.chat.id
    homework = states[chat_id]
    
    username = message.text
    user = session.query(User).filter_by(name=username).one()
    completed_homework = session.query(CompletedHomework).filter_by(student_id=user.id, homework_id=homework.id).one()
    states[chat_id] = completed_homework

    bot.send_document(message.chat.id, completed_homework.file_telegram_id)

    bot.send_message(chat_id, "Оценка за дз:")
    bot.register_next_step_handler(message, check_end)

def check_end(message):
    chat_id = message.chat.id
    completed_homework = states[chat_id]
    completed_homework.marks = int(message.text)

    session.commit()

    bot.send_message(chat_id, "Проверено")
    send_main_menu(message)


