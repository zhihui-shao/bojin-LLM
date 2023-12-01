# 用LLM提取问题中的公司名称和关键字
import json
import requests
import re

def Qwen_post(prompt):
    
    # 定义API接口的URL
    url = 'http://172.31.233.204:8001/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Qwen-7B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                        这是公司名称提取器，你要从用户输入的文本中提取公司名称。
                        公司名称是一个词，一般以“有限公司”或“股份”结尾。
                            
                        示例模板：
                        用户输入：根据浙江开尔新材料股份有限公司招股意向书，截至2010年末，合肥翰林总资产为多少？
                        浙江开尔新材料股份有限公司   
                                              
                        用户输入：昇兴集团股份有限公司因租赁厂房存在经营风险的下属企业是什么？
                        昇兴集团股份有限公司
                        
                        用户输入：截至2009年底，中海达、南方测绘合计占有国产品牌销售额的多大比例？
                        中海达
                        
                        用户输入：大博医疗科技股份有限公司在2015年受到了哪些行政处罚？
                        大博医疗科技股份有限公司
                        
                        用户输入：北京天宜上佳高新材料股份有限公司外购件有哪些？
                        北京天宜上佳高新材料股份有限公司
                        
                        用户输入：兰州海默科技股份有限公司的实际控制人是谁？
                        兰州海默科技股份有限公司
                        
                        用户输入：广州中海达卫星导航技术股份有限公司收购的对象中海达测绘的全称是什么？截至该次股权收购前，其注册资本为多少？
                        广州中海达卫星导航技术股份有限公司
                        
                        用户输入：浙江开尔新材料股份有限公司和合肥翰林是否按规定为员工缴纳了社会保险？
                        浙江开尔新材料股份有限公司


                        请按照上述示例模板，提取出公司名称。
                        注意：只需要返回公司名称即可，不用回答问题或者输出其他内容。                   
                        用户输入：{prompt}        
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0.1,
        "top_p": 0,
        "n": 1,
        "max_tokens": 512,
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

json_list = []
for obj in datas: 
    id = obj['b_id']     
    question = obj['b_question']

    company_name = Qwen_post(question)
    print(id)
    print(company_name)
    
    json_list.append({"b_id": id, "b_question": question, "company_name": company_name})
    
    
output_file = "company_name_1201.json"    # 每次循环迭代都将结果追加到JSON文件
with open(output_file, "a", encoding="utf-8") as output:
    json.dump(json_list, output, ensure_ascii=False,indent=4)
        
    
