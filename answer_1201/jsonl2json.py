import json


def jsonl_to_json(jsonl_file, json_file):
    json_data = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                json_data.append(obj)
            except json.JSONDecodeError:
                print(f"Ignoring invalid JSON object: {line}")

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


jsonl_file = './answer_1201_jieba.jsonl'
json_file = './answer_1201_jieba.json'
jsonl_to_json(jsonl_file, json_file)
