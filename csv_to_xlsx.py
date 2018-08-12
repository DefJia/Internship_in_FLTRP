"""
    Copied from https://blog.csdn.net/qq_33689414/article/details/78307031
"""

import csv
import xlwt


def csv_to_xlsx(path, file):
    with open(path + file + '.csv', 'r', encoding='utf-8') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')  # 创建一个sheet表格
        l = 0
        for line in read:
            print(line)
            r = 0
            for i in line:
                print(i)
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1

        workbook.save(path + file + '.xlsx')  # 保存Excel


if __name__ == '__main__':
    for letter in range(66, 91):
        csv_to_xlsx('Docu/Others/', chr(letter) + '_log')