import json
import os

right_sql = './merge_right_sql.json'
with open(right_sql, "r", encoding="utf-8") as file:
    right_sql_datas = json.load(file)

all_sql = '../../q_classify/A_question.json'
with open(all_sql, "r", encoding="utf-8") as file:
    all_sql_datas = json.load(file)

output_file = "no_right_sql.json"  # 每次循环迭代都将结果追加到JSON文件

my_set = set()

for obj in right_sql_datas:
    id = obj['a_id']
    my_set.add(id)

for obj in all_sql_datas:
    id = obj['a_id']
    question = obj['a_question']
    if id in my_set:
        continue

    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"a_id": id, "a_question": question, "sql": ""}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')
