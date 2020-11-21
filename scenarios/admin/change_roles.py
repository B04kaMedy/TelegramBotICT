from bot import bot
from filters import callback
from models import Role, User, Group
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu


@bot.message_handler(func=callback("Изменить роль"))
def user_select(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        markup.add(KeyboardButton(user.name))
    
    bot.send_message(message, "Выберите человека:", reply_markup=markup)
    bot.register_next_step_handler(message, change_roles)


def change_roles(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for role in Role:
        markup.add(KeyboardButton(role.value))

    bot.send_message(message, "Выберите новую роль:", reply_markup=markup)
    bot.register_next_step_handler(message, option_select)


def option_select(message):
    chat_id = message.chat.id 
    user = User.from_telegram_id(chat_id)

    # TODO:
    # if role == Role.ADMIN: ask_again_to_be_sure
    # if my_role == Role.ADMIN: reject changing (!)

    role = Role(message.text)

    message.current_group.add_role_to_user(user, role)

    bot.send_message(chat_id, "Роль пользователя'" + user.name + "' успешно изменена!")
    bot.send_message(chat_id, "Новая роль пользователя: " + str(role))
