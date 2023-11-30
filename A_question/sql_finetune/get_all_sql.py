import json

right_sql_1 = './merge_right_sql.json'
with open(right_sql_1, "r", encoding="utf-8") as file:
    right_sql_1_datas = json.load(file)

right_sql_2 = './no_right_sql.json'
with open(right_sql_2, "r", encoding="utf-8") as file:
    right_sql_2_datas = json.load(file)

output_file = "all_right_sql.json"  # 每次循环迭代都将结果追加到JSON文件

length = max(len(right_sql_1_datas), len(right_sql_2_datas))

i, j = 0, 0

while i < len(right_sql_1_datas) and j < len(right_sql_2_datas):

    if right_sql_1_datas[i]['a_id'] < right_sql_2_datas[j]['a_id']:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(right_sql_1_datas[i], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        i = i + 1
    elif right_sql_1_datas[i]['a_id'] == right_sql_2_datas[j]['a_id']:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(right_sql_1_datas[i], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        i = i + 1
        j = j + 1
    else:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(right_sql_2_datas[j], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        j = j + 1

if i == len(right_sql_1_datas):
    while j != len(right_sql_2_datas):
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(right_sql_2_datas[j], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        j = j + 1
else:
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump(right_sql_1_datas[i], output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')
    i = i + 1
