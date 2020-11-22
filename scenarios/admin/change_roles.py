from bot import bot
from db import session
from filters import callback
from models import Role, User
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu


@bot.message_handler(func=callback("Изменить роль"))
def user_select(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        markup.add(KeyboardButton(user.name))
    
    bot.send_message(chat_id, "Выберите человека:", reply_markup=markup)
    bot.register_next_step_handler(message, change_roles)


username = ''
is_checked = False


def change_roles(message):
    chat_id = message.chat.id

    global username
    username = message.text

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for role in Role:
        markup.add(KeyboardButton(role.value))

    bot.send_message(chat_id, "Выберите новую роль:", reply_markup=markup)
    bot.register_next_step_handler(message, option_select)


def option_select(message):
    chat_id = message.chat.id 
    user = session.query(User).filter_by(name=username).one()

    # FIXME:
    # if role == Role.ADMIN: ask_again_to_be_sure
    # if my_role == Role.ADMIN: reject changing (!)   <- check
    global is_checked

    if message.current_group.user_has_role(user, Role.ADMIN):
        bot.send_message(chat_id, "Вы не можете поменять себе роль, так как Вы -- администратор.")
    else:
        role = Role(message.text)

        if role == Role.ADMIN and not is_checked:
            bot.send_message(chat_id, "Вы уверены, что хотите дать этому пользователю права администратора?")
            is_checked = True
            bot.register_next_step_handler(message, option_select)
        else:
            message.current_group.add_role_to_user(user, role)

            bot.send_message(chat_id, "Роль пользователя'" + user.name + "' успешно изменена!")
            bot.send_message(chat_id, "Новая роль пользователя: " + str(role))

    if is_checked:
        is_checked = False

    send_main_menu(message)


def rejected(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вы не можете поменять себе роль, так как Вы -- администратор.")

    send_main_menu(message)
