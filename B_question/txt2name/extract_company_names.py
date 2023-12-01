# 将80个txt文档的文件名与公司名称对应起来
import requests
import os
import json

def Qwen_post(t):
    
    # 定义API接口的URL
    url = 'http://172.31.233.204:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                    你是一个能精准提取信息的AI。
                    我会给你一篇招股说明书，请输出此招股说明书的主体是哪家公司，若无法查询到，则输出无。\n
                    {t}\n\n
                    请指出以上招股说明书属于哪家公司，请只输出公司名。
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0.1,
        "top_p": 0.5,
        "n": 1,
        "max_tokens": 8192,
        "stream": False
    }

    # 发送POST请求
    response = requests.post(url, json=data)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应JSON数据
        response_data = response.json()
        # 处理响应数据
        answer = response_data.get('choices')[0].get('message').get('content')
            
        return answer
    else:
        print(f"请求失败，状态码: {response.status_code}")
        
        
# 指定目录路径
directory_path = "../../bs_challenge_financial_14b_dataset/pdf_txt_file"

# 获取目录中所有的txt文件名
txt_files = [f for f in sorted(os.listdir(directory_path)) if f.endswith('.txt')]

# 将每个文件名存为一条json数据
for file_name in txt_files:
    file_path = os.path.join(directory_path, file_name)
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        company_name = Qwen_post(content[:6000])
        print(company_name)

    # 将json数据写入文件
    with open('extract_company_names.json', 'a', encoding='utf-8') as json_file:
       json.dump({"file_name": file_name,"company_name":company_name}, json_file, ensure_ascii=False,indent=4)
       json_file.write(','+'\n')

