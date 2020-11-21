import csv
from typing import List, Dict, Optional

from excel.functions import *

_students = dict()  # type: dict[str: List[str]]
_columns = ['student']  # type: List[str]

def push_to_tmp_container(file_name: str):
    for student_name in _students:
        update_student_list(student_name)

    path = file_name

    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=_columns)
        writer.writeheader()

        def unpack_student(index: int) -> List[str]:
            res = []  # type: List[str]

            name = list(_students.keys())[index]

            res.append(name)

            for index, data in enumerate(get_student_list(name)):
                res.append(data)

            return res

        for i in range(len(_students)):
            writer.writerow(dict(zip(_columns, unpack_student(i))))


def import_from_tmp_container(file_name: str):
    with open(file_name, 'r') as csv_file:
        global _columns
        global _students

        def pack_student(strings: List[str]) -> Dict[str, List[str]]:
            student_name = strings[0]
            student_list = strings[1:]

            return {student_name: student_list}

        for index, row in enumerate(csv_file):
            row = row.rstrip('\n').split(',')

            if index == 0:
                _columns = row
            else:
                _students.update(pack_student(row))


def clear_table():
    global _columns
    global _students
    
    _students = dict()
    _columns = ['student']


def add_student(name: str) -> bool:
    if not check_student(name):
        _students.update({name: list()})

        log('Student was successfully added!')
    else:
        log('Student with a such name is already exists!')

        return False


def get_student_name_by_id(student_id: int) -> Optional[str]:
    student_names = list(_students.keys())

    if student_id >= len(student_names):
        flood('The id you gave is incorrect! '
              'Please, check your input.')
        return None

    flood('Student found.')
    return student_names[student_id]


def check_student(pointer) -> bool:
    if type(pointer) == int:
        return get_student_name_by_id(pointer) is not None
    else:
        student_names = list(_students.keys())

        return student_names.__contains__(pointer)


def get_student_list(name: str) -> Optional[List[str]]:
    if not check_student(name):
        log('There is no student with a such name!')
        return None

    flood('Student found.')

    return _students.get(name)


def update_student_list(name: str) -> List[str]:
    student_list = get_student_list(name)

    the_length = len(_columns) - 1

    if len(student_list) > the_length:
        pass
    else:
        while len(student_list) <= the_length:
            student_list.append('')

    _students.update({name: student_list})

    return student_list


def remove_student(name: str) -> bool:
    if not check_student(name):
        log('There is no student with a such name. '
            'You can not remove it!')

        return False

    _students.pop(name)

    log('Student was successfully removed')

    return True


def add_column(name: str):
    # There can be two similar columns
    _columns.append(name)

    flood('Column was successfully added!')


def find_column(name: str) -> Optional[int]:
    try:
        index = _columns.index(name)

        flood('Column found.')

        return index
    except ValueError:
        flood('There is no column with a such name!')

        return None


def remove_column(name: str) -> bool:
    index = find_column(name)

    if index is None:
        log('There is no column with a such name. '
            'You can not remove it!')

        return False
    else:
        for student_name in _students:
            update_student_list(student_name)

        _columns.remove(name)

        for student_name, student_list in _students.items():
            del student_list[index - 1]

            _students.update({student_name: student_list})

        log('Column was successfully removed!')

        return True


def review_on_student(student_name: str, cell, data: str) -> bool:
    if type(cell) == int:
        cell = cell - 1  # -column 'students'

        if cell >= len(_columns):
            log('There no column to put data in! '
                'Please, create new column before putting some data there.')
            return False

        student_list = update_student_list(student_name)

        student_list[cell] = data

        _students.update({student_name: student_list})

        log('Review was successfully uploaded!')
        return True
    else:
        return review_on_student(student_name, find_column(cell), data)
