import os
import json
import re


number_map = {
    "零": '0',
    "一": '1',
    "二": '2',
    "三": '3',
    "四": '4',
    "五": '5',
    "六": '6',
    "七": '7',
    "八": '8',
    "九": '9',
    "十": '10'
}


def chinese_to_num(str_list):
    print(str_list)
    str_list[2] = number_map.get(str_list[2])
    print(11111111111111111)
    print(str_list)
    return str_list


def change_month(str_list):
    if str_list[1] != "10" or str_list != '11' or str_list != '12':
        str_list[1] = '0' + str_list[1]
    return str_list


def my_split(id, str_list):
    if id == 23:
        new_list = str_list[1].split("公司")
        new_list[0] = new_list[0] + "公司"
    if id == 31:
        new_list = str_list[1].split("公司")
        new_list[0] = new_list[0] + "公司"
        new_list.append(str_list[2])
    return new_list


def get_quarter(str_list):
    if str_list[1] == '一':
        str_list[1] = '03-31'
    elif str_list[1] == '二':
        str_list[1] = '06-30'
    elif str_list[1] == '三':
        str_list[1] = '09-30'
    else:
        str_list[1] = '12-31'
    return str_list


def if_half_year(str_list):
    if str_list[2] == '半年度':
        str_list[2] = '0630'
    else:
        str_list[2] = '1300'
    return str_list


def get_value(str1, str2):
    p = re.compile(r'\(\d*?\)', re.S)
    new_str1 = re.findall(p, str1)

    str2_other = re.split(p, str1)
    for i in str2_other:
        str2 = str2.replace(i, '@', 1)

    str2 = str2.removeprefix('@')
    str2 = str2.removesuffix('@')
    new_str2 = str2.split('@')

    return new_str1, new_str2


file_path = '../../q_classify/A_question.json'
with open(file_path, "r", encoding="utf-8") as file:
    question_datas = json.load(file)

match_path = './sql_classify.json'
with open(match_path, "r", encoding="utf-8") as file:
    match_datas = json.load(file)

for obj in question_datas:
    a_id = obj['a_id']
    question = obj['a_question']
    answer = ""
    for match_obj in match_datas:
        if match_obj['keywords'] in question:
            print(match_obj['id'])
            new_str1, new_str2 = get_value(match_obj['question'], question)
            length = len(new_str1)
            answer = match_obj['sql']
            if match_obj['id'] == 5 or match_obj['id'] == 12:
                # 汉转数
                new_str2 = chinese_to_num(new_str2)
                print(new_str1)
                print(new_str2)
            if match_obj['id'] == 10:
                # 月份
                new_str2 = change_month(new_str2)
            if match_obj['id'] == 23 or match_obj['id'] == 31:
                # ()()
                new_str2 = my_split(match_obj['id'], new_str2)
            if match_obj['id'] == 47:
                # 季度转yyyy-mm-dd
                new_str2 = get_quarter(new_str2)
            if match_obj['id'] == 58:
                # 年度半年度
                new_str2 = if_half_year(new_str2)
            for i in range(0, length):
                answer = answer.replace(new_str1[i], new_str2[i])
                print(answer)

    output_file = "A_match_sql.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"a_id": a_id, "a_question": question, "sql": answer}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')

