import json
import requests
import time

def baichuan2_post(question):
    
    # 定义API接口的URL
    url = 'http://localhost:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": "user",
                "content": f'''
                {question}
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0,
        "top_p": 0,
        "n": 1,
        "max_tokens": 0,
        "stream": False
    }

    # 发送POST请求
    response = requests.post(url, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应JSON数据
        response_data = response.json()
        # 处理响应数据
        
        # print(response_data.get('choices')[0].get('message').get('content'))
        return response_data
    else:
        print(f"请求失败，状态码: {response.status_code}")
        
question = '你好'
answer = baichuan2_post(question)
data = answer.get('choices')[0].get('message').get('content')
print(data)
