from bot import bot
from models import Role
from filters import callback

from excel import excel_db, converter


@bot.message_handler(func=callback("Экспорт в Excel"))
def excel_export(message):
    excel_db.clear_table()

    group = message.current_group

    students = group.users
    hws = group.homeworks

    for hw in hws:
        excel_db.add_column(str(hw.id))

    for student in students:
        if not student.is_student(group):
            continue

        excel_db.add_student(student.name)

        for hw in hws:
            completed = hw.get_completed_from_student(student)
            mark = completed.mark
            comment = completed.comment

            data = str(mark)

            if comment is not None and comment != '':
                data += ', комментарий учителя: ' + comment

            excel_db.review_on_student(student.name, str(hw.id), data)

    file_name = "/tmp/mark_table.xlsx"

    converter.push_to_excel(file_name, group.name)

    bot.send_document(message.chat.id, open(file_name, 'rb'))
