from excel.converter import *
from excel.excel_db import *


def push_excel_test():
    add_column('test_column_1')
    add_column('test_column_2')

    add_student('test_student_1')
    add_student('test_student_2')

    review_on_student('test_student_2', 'test_column_2', 'test_data')

    push_to_excel('output.xlsx', 'test')


def pull_excel_test():
    get_from_excel('output.xlsx', 'test')

    add_column('test_column_1')
    remove_column('test_column_2')
    add_column('test_column_3')

    add_student('test_student_1')
    add_student('test_student_3')

    review_on_student('test_student_3', 'test_column_3', 'test_data_2')

    push_to_excel('output.xlsx', 'test')


add_column('column')

add_student('student')

review_on_student('student', 'column', 'data 1')

a = 1
while a != 0:
    review_on_student('student', 'column', str(a))
    push_to_excel('output.xlsx', 'test')
    a = int(input())

# push_excel_test()
# pull_excel_test()
