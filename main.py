import csv
import re
from logger import logger_path


def fix_name(contact):
    result = ','.join(contact[0:3]).rstrip(',').replace(' ', ',').split(',')
    while len(result) != 3:
        result.append('')
    result.extend(contact[3:])
    return result


def fix_phone(phone):
    res_1 = re.sub(r'^(\+7|8)[\s(]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})', r'+7(\2)\3-\4-\5', phone)
    result = re.sub(r'[\s(]*[а-яёА-ЯЁ]+[.\s(]*(\d+)\)*', r' доб.\1', res_1)
    return result


def fix_phonebook(contacts_list):
    result_list = []
    result_list.append(contacts_list[0])
    for line in contacts_list[1:]:
        line = fix_name(line)
        line[5] = fix_phone(line[5])
        result_list.append(line)
    return result_list


def search_doubles(fixed_list):
    double = []
    for i in enumerate(fixed_list):
        for c in enumerate(fixed_list):
            if i[0] == c[0] or i[1] in double or c[1] in double:
                continue
            else:
                if i[1][0] == c[1][0] and i[1][1] == c[1][1]:
                    double.append(i[1])
                    double.append(c[1])
                else:
                    continue
    return double


def join_doubles(doubles):
    result = []
    for i in doubles[::2]:
        result_list = []
        dic = {key: value for key, value in dict(zip(fix_phonebook(contacts_list)[0], i)).items()}
        dic.update({key: value for key, value in dict(zip(fix_phonebook(contacts_list)[0], doubles[doubles.index(i)+1])).items() if value})
        result_list.append(dic['lastname'])
        result_list.append(dic['firstname'])
        result_list.append(dic['surname'])
        result_list.append(dic['organization'])
        result_list.append(dic['position'])
        result_list.append(dic['phone'])
        result_list.append(dic['email'])
        result.append(result_list)
    return result


@logger_path('logs.json')
def clean_phonebook(contacts_list):
    step_1 = fix_phonebook(contacts_list)
    step_2 = search_doubles(step_1)
    step_3 = join_doubles(step_2)
    for items in step_2:
        step_1.remove(items)
    return step_1 + step_3


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    out = clean_phonebook(contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(out)
