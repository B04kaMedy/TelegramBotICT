from bot import bot
from models import Role, User
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def add_admin_buttons(markup):
    markup.add(KeyboardButton("Пригласить человека"))
    markup.add(KeyboardButton("Удалить человека"))

def add_teacher_buttons(markup):
    markup.add(KeyboardButton("Добавить дз"))
    markup.add(KeyboardButton("Проверить дз"))
    markup.add(KeyboardButton("Экспорт в эксель"))

def add_student_buttons(markup):
    markup.add(KeyboardButton("Посмотреть дэдлайны"))
    markup.add(KeyboardButton("Посмотреть баллы"))
    markup.add(KeyboardButton("Сдать дз"))

def send_main_menu(message):
    group = message.current_group
    user = User.from_telegram_id(message.chat.id)

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    if group.user_has_role(user, Role.ADMIN):
        add_admin_buttons(markup)
    if group.user_has_role(user, Role.TEACHER):
        add_teacher_buttons(markup)
    if group.user_has_role(user, Role.STUDENT):
        add_student_buttons(markup)

    bot.send_message(message.chat.id, f"Ваша группа: {group.name}", reply_markup=markup)