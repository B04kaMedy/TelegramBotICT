from bot import bot
from filters import callback
from models import User
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu


@bot.message_handler(func=callback("Удалить человека"))
def remove(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for user in message.current_group.users:
        markup.add(KeyboardButton(user.telegram_nickname))
    
    bot.send_message(chat_id, "Выберите человека:", reply_markup=markup)
    bot.register_next_step_handler(message, remove_success)


def remove_success(message):
    chat_id = message.chat.id
    group_name = message.current_group.name
    user = User.from_telegram_nickname(message.text)

    message.current_group.delete_user(user)
    bot.send_message(chat_id, "Пользователь удалён")

    send_main_menu(message)
