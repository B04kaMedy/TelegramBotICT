from bot import bot
from filters import callback
from models import Role, User, Group
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.main_menu import send_main_menu

@bot.message_handler(func=callback("Пригласить человека"))
def invite(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите @username")
    bot.register_next_step_handler(message, invite_success)

user_names = dict()
def invite_success(message):
    chat_id = message.chat.id
    user_names[chat_id] = message.text 

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for role in Role:
        markup.add(KeyboardButton(role.value))

    bot.send_message(chat_id, "Выдайте роль", reply_markup=markup)
    bot.register_next_step_handler(message, role_success)

current_inventation = dict()
def role_success(message):
    chat_id = message.chat.id
    username = user_names[chat_id] 
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    markup.add(KeyboardButton("Принять"))
    markup.add(KeyboardButton("Отклонить"))


    # TODO проверка зареган ли юзер

    to_user = User.from_telegram_nickname(username)

    invite_message = bot.send_message(to_user.telegram_id, f"Вас пригласили в группу {message.current_group.name}", reply_markup=markup)
    bot.register_next_step_handler(invite_message, accept_inventation)

    current_inventation[invite_message.chat.id] = (message.current_group, Role(message.text))

    send_main_menu(message)


def accept_inventation(message):
    chat_id = message.chat.id

    if message.text == "Принять":
        user = User.from_telegram_id(chat_id)
        group, role = current_inventation[chat_id]
        group.add_role_to_user(user, role)

        bot.send_message(chat_id, "Вы добавлены в группу!")

    else:
        bot.send_message(chat_id, "Окей. Отклонено.")


    