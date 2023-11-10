import os
import json

# 指定目录路径
directory_path = "../bs_challenge_financial_14b_dataset/pdf_txt_file"


# 获取目录中所有的txt文件名
txt_files = [f for f in sorted(os.listdir(directory_path)) if f.endswith('.txt')]


# 将每个文件名存为一条json数据
json_data = []
for file_name in txt_files:
    print(file_name)
    json_data.append({"file_name": file_name,"company_name":" "})

# 将json数据写入文件
with open('txt2company_name.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("JSON数据已保存。")
