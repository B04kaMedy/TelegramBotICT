from bot import bot

from db import session
from models import User, Group, Role
from scenarios.groups import set_current
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

def create_group(msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Введи название для группы")
    bot.register_next_step_handler(msg, create_group2)

names = dict()

def create_group2(msg):
    chat_id = msg.chat.id
    names[chat_id] = msg.text

    markup = ReplyKeyboardMarkup()
    markup.add("Ученик")
    markup.add("Учитель")

    bot.send_message(chat_id, "Вы ученик или учитель?", reply_markup = markup)
    bot.register_next_step_handler(msg, got_name_of_group)


def got_name_of_group(msg):
    chat_id = msg.chat.id
    name = names[chat_id]

    role = msg.text

    if role == "Ученик":
        role = Role.ADMIN_STUDENT
    else:
        role = Role.ADMIN_TEACHER

    group = Group(name=name)
    session.add(group)
    session.commit()

    user = User.from_telegram_id(chat_id)
    group.add_role_to_user(user, role)

    bot.send_message(chat_id, "Отлично, группа создана!")
    return set_current.select_group(msg)
