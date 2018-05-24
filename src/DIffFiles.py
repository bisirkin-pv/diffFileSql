# -*- coding: utf-8 -*-
import os
import re


def check(file1, file2):
    txt = ''
    with open(file1) as file:
        for num, line in enumerate(file):
            txt += line
    file_left = re.split(r'\n', txt)
    start_left_file = 0
    lag_left = 0
    # находим индекс старта процедуры в первом массиве
    for num, line in enumerate(file_left):
        if re.search(r'create[ ]+procedure', line, re.I) is not None:
            start_left_file = num
            lag_left = num - 1
    if start_left_file >= len(file_left):
        return 0

    # открываем второй файл для сравнения
    start_right_file = -1
    start_procedure = -1
    count_error = 0
    stack = []
    lag_right = 0
    with open(file2) as file:
        for num, line in enumerate(file):
            if re.search(r'create[ ]+procedure', line, re.I) is not None:
                start_right_file = num
                lag_right = num + 1
            if start_right_file < 0:
                continue
            # начало и конец процедуры определяем в рамках BEGIN END
            res = re.search(r'(begin|case)\b', file_left[start_left_file], re.I)
            if res is not None:
                start_procedure = 1
                stack.append(res[0])
            res = re.search(r'(end)\b', file_left[start_left_file], re.I)
            if res is not None:
                stack.pop()
            if start_procedure > 0 and len(stack) == 0:
                break
            # начинаем проверку когда есть два начала процедуры
            count_error += diff(file_left, start_left_file, line, num, lag_left, lag_right)
            start_left_file += 1
            if start_left_file >= len(file_left):
                break
        return count_error


def diff(left, l_start, right, r_start, lag_left, lag_right):
    # Это для удобаства отображения
    left_txt = re.sub(r' ', u"\u2022", left[l_start])
    left_txt = re.sub(r'\t', '/t', left_txt)
    right_text = re.sub(r'\n', '', right) # Данная замена обязательная
    right_text = re.sub(r' ', u"\u2022", right_text)
    right_text = re.sub(r'\t', '/t', right_text)
    if left_txt != right_text:
        print('\tLine {0} in file left not equal line {1} in file right'.format(l_start + lag_left
                                                                                , r_start + lag_right
                                                                                )
              )
        print('\t\tLine left :{0}'.format(left_txt))
        print('\t\tLine right:{0}'.format(right_text))
        return 1
    return 0


if __name__ == "__main__":
    file1 = "../test2.txt"
    file2 = "../test.txt"
    file_name_left = os.path.splitext(os.path.basename(file2))[0]
    file_name_right = os.path.splitext(os.path.basename(file1))[0]
    print('Check file left: {0}, right: {1}'.format(file_name_left, file_name_right))
    print('-'*150)
    check(file1, file2)

