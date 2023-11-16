# 用LLM生成问题的回答模板
import json
import requests
import re

def Qwen_post(question):
    
    # 定义API接口的URL
    url = 'http://localhost:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                        这是模板生成器，你要从用户输入的文本中生成回答模板。
                        模板要求：尽量保留用户输入的原话，将问句改为陈述句，并保留占位符用于填充正确答案。
                        输出完毕后结束，不要生成新的用户输入，不要新增内容。
                        
                        示例：
                        用户输入：截至2011年，内蒙古君正能源化工股份有限公司正在从事的研发项目有哪些？
                        截至2011年，内蒙古君正能源化工股份有限公司正在从事的研发项目有()。
                        用户输入：请帮我查询出20210415日，建筑材料一级行业涨幅超过5%（不包含）的股票数量。
                        20210415日，建筑材料一级行业涨幅超过5%（不包含）的股票数量是()。
                        用户输入：广州中海达卫星导航技术股份有限公司收购的对象中海达测绘的全称是什么？截至该次股权收购前，其注册资本为多少？
                        广州中海达卫星导航技术股份有限公司收购的对象中海达测绘的全称是()，截至该次股权收购前，其注册资本为()。     
                        用户输入：请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                        在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是()，涨跌幅是()。

                        ###
                        用户输入：{question}
                        ###
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0,
        "top_p": 0,
        "n": 1,
        "max_tokens": 2048,
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
        
        
file_path = '../bs_challenge_financial_14b_dataset/question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   

for obj in datas: 
    id = obj['id']     
    question = obj['question']
    answer_template = Qwen_post(question)
    answer_template = answer_template.strip()
    print(answer_template)

    output_file = "answer_template.json"    # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"id":id , "question": question,"answer_template":answer_template}, output, ensure_ascii=False,indent=4)
        output.write(','+'\n')