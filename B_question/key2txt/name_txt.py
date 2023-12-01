# 国科微电子   湖南国科微电子股份有限公司
# 宁波华瑞   华瑞电器股份有限公司
# 华瑞股份   华瑞电器股份有限公司
# 中海达   广州中海达卫星导航技术股份有限公司
# 真兰仪表    上海真兰仪表科技股份有限公司
# 南岭化工厂   湖南南岭民用爆破器材股份有限公司
# 勤上有限    东莞勤上光电股份有限公司
# 旷达汽车织物集团    江苏旷达汽车织物集团股份有限公司

    
#         "b_question": "生态环境建设行业的上游是什么行业？",
#     "keywords": " 生态环境建设行业、上游行业"

import json
import re

file_path_1 = '../get_keywords/company_name_1201.json'
with open(file_path_1, "r", encoding="utf-8") as file:
    datas = json.load(file)   

file_path_2 = '../txt2name/txt2company_name.json'
with open(file_path_2, "r", encoding="utf-8") as txt2c_file:
    txt_company_data = json.load(txt2c_file)  
# print(type(txt_company_data))    

json_list = []
for obj in datas: 
    id = obj['b_id']    
    question = obj['b_question'] 
    c_name = obj['company_name'].strip()


    if '国科微电子' in c_name:
        c_name = "湖南国科微电子股份有限公司"
    elif "宁波华瑞" in c_name:
        c_name = "华瑞电器股份有限公司"
    elif "华瑞股份" in c_name:
        c_name = "华瑞电器股份有限公司"
    elif "中海达" in c_name:
        c_name = "广州中海达卫星导航技术股份有限公司"
    elif "真兰仪表" in c_name:
        c_name = "上海真兰仪表科技股份有限公司"
    elif "南岭化工厂" in c_name:
        c_name = "湖南南岭民用爆破器材股份有限公司"
    elif "勤上有限" in c_name:
        c_name = "东莞勤上光电股份有限公司"
    elif "旷达汽车织物集团" in c_name:
        c_name = "江苏旷达汽车织物集团股份有限公司"

    
    print(id)
    print(c_name)      

    for line in txt_company_data:
        company_name = line["company_name"].strip()
        if c_name in company_name:
            txt_name = line["file_name"]
            print("=======================")
            break
        else:
            txt_name = ""
    
    json_list.append({"b_id":id , "b_question": question,"company_name":c_name,"txt_name":txt_name})
    
                
output_file = "c2txt_1201.json"    # 每次循环迭代都将结果追加到JSON文件
with open(output_file, "a", encoding="utf-8") as output:
    json.dump(json_list, output, ensure_ascii=False,indent=4)
