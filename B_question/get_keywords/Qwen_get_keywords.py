# 用LLM提取问题中的公司名称和关键字
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
                        这是文字提取器，你要从用户输入的文本中提取关键词。
                        关键词是指：问题最终指向的词语，通常是名词或句子的宾语，通常出现在公司名称或时间状语后面。
                        如：净利润、部门、主营业务、实际控制人、注册资本、发明专利、英文名称、原材料、毛利率、营业收入、在册员工、
                        主要产品、法定代表人、子公司、有效期、所处行业、在册员工、发起人、控股股东、增长幅度，收入比重、销售额占营业收入的比例、
                        人工成本占业务成本的比例、无。
                        对象可以有多个，没有写“无”。
                        输出完毕后结束，不要生成新的用户输入，不要新增内容。
                        
                        示例模版：
                        用户输入：浙江双飞无油轴承股份有限公司目前的主要产品应用在哪些下游领域？
                        浙江双飞无油轴承股份有限公司、主要产品、下游领域
                        用户输入：海南双成药业股份有限公司的前身是什么？成立于何时？
                        海南双成药业股份有限公司、成立时间
                        用户输入：西安启源机电装备股份有限公司的核心产品铁芯剪切设备的收入比重从2007年度和2009年度分别为多少？
                        西安启源机电装备股份有限公司、铁芯剪切设备、收入比重、2007年、2009年
                        用户输入：截至2016年6月30日，华达汽车科技股份有限公司及子公司共有技术研发人员多少人？技术研发人占员工总人数的多大比例？
                        2016年6月30日、华达汽车科技股份有限公司、子公司、技术研发人员、员工总人数

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
        
file_path = '../../q_classify/B_question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   

for obj in datas: 
    id = obj['b_id']     
    question = obj['b_question']
    match = False
    while not match:
        answer = Qwen_post(question)
        print(answer)
        pattern = r'、' 
        match = re.search(pattern, answer)
        
    output_file = "B_keywords.json"    # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"b_id":id , "b_question": question,"keywords":answer}, output, ensure_ascii=False,indent=4)
        output.write(','+'\n')
        
    
