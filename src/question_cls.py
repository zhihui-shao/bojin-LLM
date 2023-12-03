import json
import re

def questions_classify():
    file_path = './question.json'
    with open(file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)   
    A_questions = []
    B_questions = []
   
    for obj in datas:
        id = obj["id"]
        question = obj["question"]
        
        pattern = r'[0-9]{6,}|小数点|收益率|\d{4}-\d{2}-\d{2}|机构投资者|基金|日波动值' 
        match = re.search(pattern, question)
        if match and ('加权平均净资产' not in question):
            print(question)
            A_questions.append({"a_id":id , "a_question": question})
        else:
            B_questions.append({"b_id":id ,"b_question": question})
     
            
    A_file = "A_question.json"    
    with open(A_file, "w", encoding="utf-8") as A_output:
        json.dump(A_questions, A_output, ensure_ascii=False,indent=4)
                                  
    B_file = "B_question.json"    
    with open(B_file, "w", encoding="utf-8") as B_output:
        json.dump(B_questions, B_output, ensure_ascii=False,indent=4)

