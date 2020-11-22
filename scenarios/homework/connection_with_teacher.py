from bot import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types
from models import User, Role
from db import session
from filters import callback
from scenarios.main_menu import send_main_menu


@bot.message_handler(func=callback("Написать преподавателю"))
def choose_teacher(message):
    chat_id = message.chat.id

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        if user.is_teacher(message.current_group):
            markup.add(KeyboardButton(user.name))

    bot.send_message(chat_id, "Кому Вы хотите написать?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_teacher)


usernames = dict()


def ask_teacher(message):
    chat_id = message.chat.id
    answer = message.text

    if answer == 'Отмена':
        send_main_menu(message)
    else:
        global username

        usernames[chat_id] = answer

        bot.send_message(chat_id, 'Что бы Вы хотели спросить у своего любимого преподавателя? :)')

        bot.register_next_step_handler(message, the_question)


def the_question(message):
    chat_id = message.chat.id
    msg = message.text

    # user = User.from_telegram_nickname(usernames[chat_id])
    user = session.query(User).filter_by(name=usernames[chat_id]).one()

    me = User.from_telegram_id(chat_id)
    # user.inbox = str(user.inbox) + '\n' + 'новое сообщение от \'' + me.name + '\': ' + msg

    # session.commit()
    
    bot.send_message(user.telegram_id, f"Сообщение от пользователя {me.name}:\n{msg}")
    bot.send_message(chat_id, "Сообщение отправлено!")

    send_main_menu(message)


@bot.message_handler(func=callback("Проверить входящие сообщения"))
def check_inbox(message):
    chat_id = message.chat.id
    user = User.from_telegram_id(chat_id)

    if user.is_inbox_empty():
        bot.send_message(chat_id, 'У вас нет новых сообщений :(')
    else:
        bot.send_message(chat_id, user.inbox)
        user.inbox = ''

    send_main_menu(message)
