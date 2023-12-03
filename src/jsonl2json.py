import json


def jsonl_to_json():
    jsonl_file = '../bs_challenge_financial_14b_dataset/question.json'
    json_file = 'question.json'
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

