from bot import bot
from telebot import types
from models import Homework, Group, CompletedHomework, User, Role
from db import session
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from filters import callback
from scenarios.main_menu import send_main_menu

from excel import excel_db, converter

@bot.message_handler(func=callback("Экспорт в эксель"))
def excel_export(message):
    excel_db.clear_table()

    group = message.current_group

    students = group.users
    hws = group.homeworks

    marks = dict()

    for hw in hws:
        excel_db.add_column(str(hw.id))

    for student in students:
        if not group.user_has_role(student, Role.STUDENT):
            continue

        excel_db.add_student(student.name)

        for hw in hws:
            completed = hw.get_completed_from_student(student)
            mark = completed.marks

            excel_db.review_on_student(student.name, str(hw.id), str(mark))

    file_name = "/tmp/mark_table.xlsx"

    converter.push_to_excel(file_name, group.name)

    bot.send_document(message.chat.id, open(file_name, 'rb'))
