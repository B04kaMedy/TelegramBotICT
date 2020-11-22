from bot import bot
from models import User
from db import session
from filters import not_authorized
import re


@bot.message_handler(func=not_authorized)
def new_user(msg):
    start_register(msg)


from scenarios.groups.set_current import select_group


def start_register(msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Привет! Зарегистрируся.")
    bot.send_message(chat_id, "Для того, чтобы учителя или ученики могли тебя опознать, введи, пожалуйста, ФИО")
    bot.register_next_step_handler(msg, fio)


def fio(msg):
    chat_id = msg.chat.id
    name = msg.text

    # проверка корректности ФИО
    a = 0
    name_split = name.split(" ")
    while a == 0:
        if bool(re.search('[а-яА-Я]', name)) and len(name_split) == 3:
            a == 1
        else:
            bot.send_message(chat_id, "Пожалуйста, используйте буквы только русского алфавита.")
            bot.send_message(chat_id, "Имя должно быть в формате <Фамилия Имя Отчество>")
            bot.register_next_step_handler(msg, fio)
            return
        a = 1
    #

    user = User(
        name=name,
        telegram_id=chat_id,
        telegram_nickname=msg.from_user.username
    )
    session.add(user)
    session.commit()

    bot.send_message(chat_id, "Отлично, теперь ты в системе!")
    return select_group(msg)

