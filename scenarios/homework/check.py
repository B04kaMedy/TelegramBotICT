from bot import bot
from telebot import types
from models import Homework, CompletedHomework, User
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

    hws = homework.completed_homeworks  # type: list
    hws.sort(key=lambda e: e.is_checked())

    for hw in hws:
        button_name = hw.student.name

        if hw.is_checked():
            button_name += ' (+)'

        markup.add(KeyboardButton(button_name))

    bot.send_message(chat_id, "Выберите ученика", reply_markup=markup)
    bot.register_next_step_handler(message, check_next2)


def check_next2(message):
    chat_id = message.chat.id
    homework = states[chat_id]
    
    username = message.text  # type: str

    if username.endswith(' (+)'):
        username = username[:-4]

    user = session.query(User).filter_by(name=username).one()
    completed_homework = session.query(CompletedHomework).filter_by(student_id=user.id, homework_id=homework.id).one()
    states[chat_id] = completed_homework

    bot.send_document(message.chat.id, completed_homework.file_telegram_id)

    bot.send_message(chat_id, "Оценка за дз:")
    bot.register_next_step_handler(message, check_next3)


def check_next3(message):
    chat_id = message.chat.id
    completed_homework = states[chat_id]
    completed_homework.mark = int(message.text)

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    markup.add(KeyboardButton('Да'))
    markup.add(KeyboardButton('Нет'))

    bot.send_message(chat_id, "Хотите ли Вы оставить комментарий?", reply_markup=markup)
    bot.register_next_step_handler(message, check_next4)


any_messages = False


def check_next4(message):
    chat_id = message.chat.id

    global any_messages

    if message.text == 'Нет':
        any_messages = False
    else:
        any_messages = True
        bot.send_message(chat_id, "Ваш комментарий:")

    bot.register_next_step_handler(message, check_next4)


def check_end(message):
    chat_id = message.chat.id
    completed_homework = states[chat_id]

    if any_messages:
        completed_homework.comment = message.text
    else:
        completed_homework.comment = None

    session.commit()

    bot.send_message(chat_id, "Проверено")
    send_main_menu(message)
