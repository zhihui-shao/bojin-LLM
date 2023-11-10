import json
import re

file_path = '../bs_challenge_financial_14b_dataset/question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   
    
for obj in datas:
    id = obj["id"]
    question = obj["question"]
    pattern = r'[0-9]{6,}|小数点|收益率|\d{4}-\d{2}-\d{2}|机构投资者|基金|日波动值' 
    match = re.search(pattern, question)
    if match:
        print(question)
        
        output_file = "A_question.json"    # 每次循环迭代都将结果追加到JSON文件
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump({"a_id":id , "a_question": question}, output, ensure_ascii=False,)
            output.write(','+'\n')
    
    else:
        output_file = "B_question.json"    # 每次循环迭代都将结果追加到JSON文件
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump({"b_id":id ,"b_question": question}, output, ensure_ascii=False,)
            output.write(','+'\n')
