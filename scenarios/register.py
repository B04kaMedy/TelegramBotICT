from bot import bot
from models import User
from db import session
from filters import not_authorized

@bot.message_handler(func=not_authorized)
def new_user(msg):
	start_register(msg)

from scenarios.groups.set_current import select_group

def start_register(msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Привет, нада регаца!")
    bot.send_message(chat_id, "Для того, чтобы учителя или ученики могли тебя опознать, введи пж ФИО")
    bot.register_next_step_handler(msg, fio)

def fio(msg):
    chat_id = msg.chat.id
    name = msg.text

    # TODO: хоть какая-то проверка корректности ФИО

    user = User(
        name=name,
        telegram_id=chat_id
    )
    session.add(user)
    session.commit()

    bot.send_message(chat_id, "Отлично, тебя зарегали!")
    return select_group(msg)
