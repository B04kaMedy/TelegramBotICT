from bot import bot

from db import session
from models import User, Group, Role
from scenarios.groups import set_current


def create_group(msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Введи название для группы")
    bot.register_next_step_handler(msg, got_name_of_group)


def got_name_of_group(msg):
    chat_id = msg.chat.id
    name = msg.text
    
    group = Group(name=name)
    session.add(group)
    session.commit()

    user = User.from_telegram_id(chat_id)
    group.add_role_to_user(user, Role.ADMIN)

    return set_current.select_group(msg)
