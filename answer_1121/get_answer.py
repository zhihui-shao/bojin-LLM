import json

template_file_path = '../answer_1121/answer_template.json'
with open(template_file_path, "r", encoding="utf-8") as file:
    template_datas = json.load(file)

answer_file_path = '../answer_1121/A_answer_1121.json'
with open(answer_file_path, "r", encoding="utf-8") as file:
    answer_datas = json.load(file)

for obj in answer_datas:
    id = obj['id']
    template_datas[id] = obj

output_file = "answer_1121.json"  # 每次循环迭代都将结果追加到JSON文件
with open(output_file, "a", encoding="utf-8") as output:
    json.dump(template_datas, output, ensure_ascii=False, indent=4)
    output.write(',' + '\n')
