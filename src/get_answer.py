import json
import jsonline


def merge_file():

    A_file_path = './A_final_answer.json'
    with open(A_file_path, "r", encoding="utf-8") as file:
        A_datas = json.load(file)

    B_file_path = './B_final_answer.json'
    with open(B_file_path, "r", encoding="utf-8") as file:
        B_datas = json.load(file)

    output_file = "final_answer.json"  # 每次循环迭代都将结果追加到JSON文件
    output_datas = []

    length = max(len(A_datas), len(B_datas))

    i, j = 0, 0

    while i < len(A_datas) and j < len(B_datas):

        if A_datas[i]['id'] < B_datas[j]['id']:
            output_datas.append(A_datas[i])
            i = i + 1
        elif A_datas[i]['id'] == B_datas[j]['id']:
            output_datas.append(A_datas[i])
            i = i + 1
            j = j + 1
        else:
            output_datas.append(B_datas[j])
            j = j + 1

    if i == len(A_datas):
        while j != len(B_datas):
            output_datas.append(B_datas[j])
            j = j + 1
    else:
        output_datas.append(A_datas[i])
        i = i + 1

    with open(output_file, "a", encoding="utf-8") as output:
        json.dump(output_datas, output, ensure_ascii=False, indent=4)


def json2jsonl():
    # 读取原始JSON文件
    with open("./final_answer.json", "r", encoding="utf-8") as file:
        original_json = json.load(file)

    # 转换为JSON Lines格式
    json_lines = [{"id": item["id"], "question": item["question"], "answer": item["answer"]} for item in original_json]

    # 将转换后的数据写入文件
    with open("final_answer.jsonl", "w", encoding="utf-8") as file:
        for line in json_lines:
            json.dump(line, file, ensure_ascii=False)
            file.write('\n')


