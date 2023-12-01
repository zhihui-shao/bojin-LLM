import json
import os
from itertools import groupby


def adjust():
    json_file = './finetune_sql_1201.json'
    with open(json_file, "r", encoding="utf-8") as file:
        datas = json.load(file)

    for obj in datas:
        if "题目：" in obj["question"]:
            text_list = obj["question"].split("题目：")
            obj["question"] = text_list[1].strip().replace('#', '').replace('\n', '')
        obj["question"] = obj["question"].strip().replace('#', '').replace('\n', '')

    output_file = './finetune_sql_1202.json'
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(datas, output, ensure_ascii=False, indent=4)


def statis():
    source_sql = './finetune_sql_1202.json'
    with open(source_sql, "r", encoding="utf-8") as file:
        source_datas = json.load(file)

    data_length = len(source_datas)

    list_i = list(range(0, data_length - 1))
    for i in list_i:
        list_j = list(range(i + 1, data_length))
        for j in list_j:
            if source_datas[i] == source_datas[j]:
                print(1)
                source_datas.pop(j)
                data_length = data_length - 1
                list_i.pop()
                list_j.pop()

    with open(source_sql, 'w', encoding='utf-8') as f:
        json.dump(source_datas, f, ensure_ascii=False, indent=4)


adjust()
statis()
