from bot import bot
from filters import callback
from models import Role, User, Group
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Удалить человека"))
def remove(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        markup.add(KeyboardButton(user))
    
    bot.send_message(message, "Выберите человека:")
    bot.register_next_step_handler(message, remove_success)

def remove_success(message):
    chat_id = message.chat.id
    