import json

# 读取原始JSON文件
with open("../answer_1201/answer_1201.json", "r", encoding="utf-8") as file:
    original_json = json.load(file)

# 转换为JSON Lines格式
json_lines = [{"id": item["id"], "question": item["question"],"answer":item["answer"]} for item in original_json]

# 将转换后的数据写入文件
with open("../answer_1201/answer_1201.jsonl", "w", encoding="utf-8") as file:
    for line in json_lines:
        json.dump(line, file, ensure_ascii=False)
        file.write('\n')
