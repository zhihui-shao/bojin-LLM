import json


json_file = './finetune_sql.json'
with open(json_file, "r", encoding="utf-8") as file:
    datas = json.load(file)

for obj in datas:
    if "题目：" in obj["question"]:
        text_list = obj["question"].split("题目：")
        obj["question"] = text_list[1]

with open(json_file, "w", encoding="utf-8") as output:
    json.dump(datas, output, ensure_ascii=False, indent=4)
