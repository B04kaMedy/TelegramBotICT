from bot import bot
from models import User
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios.groups import create
from scenarios.main_menu import send_main_menu

# dict: chat_id -> current group object
current_groups = dict()
# TODO: уебать это отседова в бд

def has_not_group(message):
    # бля крч какого-то хуя middleware не работают, фиксим велосипедами
    # TODO поменять на middleware
    message.current_group = current_groups.get(message.chat.id)
    return message.chat.id not in current_groups.keys()

@bot.message_handler(func=has_not_group)
def select_group(message):
    chat_id = message.chat.id
    user = User.from_telegram_id(chat_id)

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for group in user.groups:
        markup.add(KeyboardButton(group.name))

    markup.add(KeyboardButton("Создать группу"))
    bot.send_message(chat_id, "Выбери группу, в которой будешь ща работать\nНу или сам создай свою. Ы", reply_markup=markup)
    bot.register_next_step_handler(message, got_group)

def got_group(message):
    if message.text == "Создать группу":
        return create.create_group(message)
    
    user = User.from_telegram_id(message.chat.id)
    groups = {group.name: group for group in user.groups}

    if message.text in groups.keys():
        current_groups[message.chat.id] = groups[message.text]
        message.current_group = groups[message.text]
        send_main_menu(message)
    else:
        return select_group(message)