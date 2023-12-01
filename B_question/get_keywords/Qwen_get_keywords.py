# 用LLM提取问题中的公司名称和关键字
import json
import requests
import re

def Qwen_post(question):
    
    # 定义API接口的URL
    url = 'http://172.31.233.204:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                        这是关键词提取器，你要从用户输入的文本中提取关键词。
                        关键词通常是名词或句子的宾语。
                        如：2010年6月30日、2017年、净利润、部门、主营业务、实际控制人、注册资本、发明专利、英文名称、原材料、毛利率、营业收入、在册员工、
                        主要产品、法定代表人、子公司、有效期、所处行业、在册员工、发起人、控股股东、增长幅度，收入比重、销售额、营业收入、
                        人工成本、业务成本等。
                        关键词可以有多个，每个关键字之间用“、”隔开。
                        输出完毕后结束，不要生成新的用户输入，不要新增内容。
                        \n
                        示例模版：    
                        用户输入：根据联化科技股份有限公司招股意见书，精细化工产品的通常利润率是多少？
                        联化科技股份有限公司、精细化工产品、通常利润率
                        
                        用户输入：根据东莞勤上光电股份有限公司招股意向书，全球率先整体用LED路灯替换传统路灯的案例是？
                        东莞勤上光电股份有限公司、全球、LED路灯、传统路灯
                        
                        用户输入：根据《CRCC产品认证实施规则》，《铁路产品认证证书》有效期为多久？北京天宜上佳高新材料股份有限公司取得 《铁路产品认证证书》后，至少多久需要接受一次监督？
                        《CRCC产品认证实施规则》、《铁路产品认证证书》、有效期、北京天宜上佳高新材料股份有限公司、 《铁路产品认证证书》、监督
                        
                        用户输入：截至2016年6月30日，华达汽车科技股份有限公司及子公司共有技术研发人员多少人？技术研发人占员工总人数的多大比例？
                        2016年6月30日、华达汽车科技股份有限公司、子公司、技术研发人员、员工总人数
                        
                        用户输入：2005年、2006年和2007年，宁波立立电子股份有限公司所获政府补助计入当期损益的金额分别占当年利润总额的比例是多少？
                        2005年、2006年、2007年、宁波立立电子股份有限公司、政府补助、当期损益、当年利润总额

                        用户输入：根据招股意向书，预计昇兴集团股份有限公司2015年1-3月实现净利润的范围是？
                        昇兴集团股份有限公司、2015年1-3月、净利润
                        
                        用户输入：华瑞股份第二次股权转让引入的外部投资者是？
                        华瑞股份、第二次股权转让、外部投资者

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
        "max_tokens": 1024,
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
    if id > 450:
        match = False
        while not match:
            answer = Qwen_post(question)
            print(id)
            print(answer)
            pattern = r'、' 
            match = re.search(pattern, answer)
            
        output_file = "B_keywords_1201.json"    # 每次循环迭代都将结果追加到JSON文件
        with open(output_file, "a", encoding="utf-8") as output:
            json.dump({"b_id":id , "b_question": question,"keywords":answer}, output, ensure_ascii=False,indent=4)
            output.write(','+'\n')
        
    
