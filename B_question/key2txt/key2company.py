# 国科微电子   湖南国科微电子股份有限公司
# 宁波华瑞   华瑞电器股份有限公司
# 华瑞股份   华瑞电器股份有限公司
# 中海达   广州中海达卫星导航技术股份有限公司
# 真兰仪表    上海真兰仪表科技股份有限公司
# 南岭化工厂   湖南南岭民用爆破器材股份有限公司
# 勤上有限    东莞勤上光电股份有限公司
# 旷达汽车织物集团    江苏旷达汽车织物集团股份有限公司

#     "b_question": "获得多少项国内专利？其中有多上项发明专利？",
#     "keywords": " 获得、国内专利、发明专利"
    
#         "b_question": "生态环境建设行业的上游是什么行业？",
#     "keywords": " 生态环境建设行业、上游行业"

import json
import re

file_path_1 = '../get_keywords/B_keywords_1126.json'
with open(file_path_1, "r", encoding="utf-8") as file:
    datas = json.load(file)   

file_path_2 = '../txt2name/txt2company_name.json'
with open(file_path_2, "r", encoding="utf-8") as txt2c_file:
    txt_company_data = json.load(txt2c_file)  
# print(type(txt_company_data))    

for obj in datas: 
    id = obj['b_id']    
    question = obj['b_question'] 
    keywords = obj["keywords"]
    pattern = re.compile(r'\b\w+有限公司\b')
    c_name = pattern.findall(keywords)
    
    if c_name == []:
        if '国科微电子' in keywords:
            c_name = ["湖南国科微电子股份有限公司"]
        elif "宁波华瑞"in keywords:
            c_name = ["华瑞电器股份有限公司"]
        elif "华瑞股份" in keywords:
            c_name = ["华瑞电器股份有限公司"]
        elif "中海达" in keywords:
            c_name = ["广州中海达卫星导航技术股份有限公司"]
        elif "真兰仪表" in keywords:
            c_name = ["上海真兰仪表科技股份有限公司"]
        elif "南岭化工厂" in keywords:
            c_name = ["湖南南岭民用爆破器材股份有限公司"]
        elif "勤上有限" in keywords:
            c_name = ["东莞勤上光电股份有限公司"]
        elif "旷达汽车织物集团" in keywords:
            c_name = ["江苏旷达汽车织物集团股份有限公司"]
        else:
            c_name = [""]
    
    # print(c_name[0])      

    for line in txt_company_data:
        company_name = line["company_name"]
        if company_name == c_name[0]:
            txt_name = line["file_name"]
            print("=======================")
            break
        else:
            txt_name = ""
                
    output_file = "B_kw2txt_1126.json"    # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"b_id":id , "b_question": question,"keywords":keywords,"company_name":c_name[0],"txt_name":txt_name}, output, ensure_ascii=False,indent=4)
        output.write(','+'\n')
