import json

gpt_right_sql = '../check_sql/A_gpt_right_sql_2.json'
with open(gpt_right_sql, "r", encoding="utf-8") as file:
    gpt_right_sql_datas = json.load(file)

qwen_right_sql = '../sql_get_answer/A_Qwen_sql_answer.json'
with open(qwen_right_sql, "r", encoding="utf-8") as file:
    qwen_right_sql_datas = json.load(file)

output_file = "merge_right_sql.json"  # 每次循环迭代都将结果追加到JSON文件

length = max(len(gpt_right_sql_datas), len(qwen_right_sql_datas))

i, j = 0, 0

while i != len(gpt_right_sql_datas) or j != len(qwen_right_sql_datas):

    if gpt_right_sql_datas[i]['a_id'] < qwen_right_sql_datas[j]['a_id']:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(gpt_right_sql_datas[i], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        i = i + 1
    elif gpt_right_sql_datas[i]['a_id'] == qwen_right_sql_datas[j]['a_id']:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(gpt_right_sql_datas[i], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        i = i + 1
        j = j + 1
    else:
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(qwen_right_sql_datas[j], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        j = j + 1

if i == len(gpt_right_sql_datas):
    while j != len(qwen_right_sql_datas):
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump(qwen_right_sql_datas[j], output, ensure_ascii=False, indent=4)
            output.write(',' + '\n')
        j = j + 1
else:
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump(gpt_right_sql_datas[i], output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')
    i = i + 1
