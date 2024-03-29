import re

from collections import defaultdict

# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_list_final = []


def reformat_tel(tel):
    pattern = r"(\+7|8)?\s*\(?(\d{3,3})\)?[\s-]*(\d{3,3})[\s-]*(\d{2,2})[\s-]*(\d{2,2})\s*\(?(доб.)?(\s*)?(\d+)?\)?"
    res = re.sub(pattern, r"+7(\2)\3-\4-\5 \6\8", tel)
    return res


def reformat_list(our_list):
    data = defaultdict(list)

    for info in our_list:
        key = tuple(info[:2])
        for item in info:
            if item not in data[key]:
                data[key].append(item)

    final_list = list(data.values())
    return final_list


for contact in contacts_list:
    fio = " ".join(contact[:2]).strip().split(" ")
    if len(fio) < 3:
        fio.append("")

    fio.append(contact[3])
    fio.append(contact[4])

    # приводим номер телефона к одному формату
    result = reformat_tel(contact[5])
    fio.append(result)

    fio.append(contact[6])

    contacts_list_final.append(fio)

# группируем список по фио
new_list = reformat_list(contacts_list_final)
print(new_list)

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(new_list)
