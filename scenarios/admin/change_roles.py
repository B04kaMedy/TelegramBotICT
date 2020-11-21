from bot import bot
from filters import callback
from models import Role, User, Group
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Изменить роли"))
def change_roles(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        markup.add(KeyboardButton(user))
    
    bot.send_message(message, "Выберите человека:", reply_markup=markup)
    bot.register_next_step_handler(message, user_select)

def user_select(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    markup.add(KeyboardButton("Добавить"))
    markup.add(KeyboardButton("Удалить"))

    bot.send_message(message, "Выберите желаемое действие с ролью", reply_markup=markup)
    bot.register_next_step_handler(message, option_select)
    
def option_select(message):
    chat_id = message.chat.id 
    # markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    pass
    # if message.text == "Добавить":
    #     pass