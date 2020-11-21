import csv
import os
from xlsxwriter.workbook import Workbook
import xlrd
from excel_db import *
# import pandas as pd
# import openpyxl


def remove_tmp_container(file_name: str) -> bool:
    try:
        os.remove(file_name)

        flood('The file was successfully deleted.')

        return True
    except FileNotFoundError:
        flood('This file \'' + file_name + '\' does not exits. You can not remove it!')
        return False


def csv_to_excel(csv_file_name: str, excel_file_name: str, sheet_name: str):
    workbook = Workbook(excel_file_name)
    worksheet = workbook.add_worksheet(name=sheet_name)

    with open(csv_file_name, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()


def excel_to_csv(excel_file_name: str, sheet_name: str, csv_file_name: str):
    workbook = xlrd.open_workbook(excel_file_name)

    csv_file = open(csv_file_name, 'w')

    sheet = workbook.sheet_by_name(sheet_name)

    for row in sheet.get_rows():
        lst = list(row)

        lst = [str(e.value) for e in lst]

        csv_file.write(','.join(lst) + '\n')

    csv_file.close()

    """
    xlsx = openpyxl.load_workbook(excel_path + '.xlsx')

    sheet = xlsx.active

    data = sheet.rows

    csv_file = open(excel_path + '_' + 'output.csv', 'w+')

    for row in data:
        l = list(row)
        for i in range(len(l)):
            if i == len(l) - 1:
                csv_file.write(str(l[i].value))
            else:
                csv_file.write(str(l[i].value) + ',')
            csv_file.write('\n')

    csv_file.close()
    """

    # data_xls = pd.read_excel(excel_path + '.xlsx', sheet_name, index_col=None)
    # data_xls.to_csv(excel_path + '_' + sheet_name + '.csv', encoding='utf-8')

    """
    wb = xlrd.open_workbook(excel_path + '.xlsx')
    sh = wb.sheet_by_name(sheet_name)

    your_csv_file = open(excel_path + '_' + sheet_name + '.csv', 'wb')
    wr = csv_file.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
    """


def push_to_excel(excel_file_name: str, sheet_name: str):
    tmp_container_name = 'tmp.csv'

    remove_tmp_container(excel_file_name)

    push_to_tmp_container(tmp_container_name)

    csv_to_excel(tmp_container_name, excel_file_name, sheet_name)

    remove_tmp_container(tmp_container_name)


def get_from_excel(excel_file_name: str, sheet_name: str):
    tmp_container_name = 'tmp.csv'

    excel_to_csv(excel_file_name, sheet_name, tmp_container_name)

    import_from_tmp_container(tmp_container_name)

    remove_tmp_container(tmp_container_name)
