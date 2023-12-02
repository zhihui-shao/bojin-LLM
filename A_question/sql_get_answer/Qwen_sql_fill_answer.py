# 用LLM提取问题中的公司名称和关键字
import json
import requests


def Qwen_post(question, template, answer_list):
    # 定义API接口的URL
    url = 'http://172.31.233.204:8001/v1/chat/completions'

    content = f'''
                        你是一位金融咨询专家，给你一个题目和答案列表，你需要根据题目所要求的数据格式，如小数点位数、百分比、是否取整等，参考示例，将答案列表结合问题，生成语义通顺且符合题目要求的答案。
                        请注意，你所给出的结果必须结合题目和答案列表，不要有任何额外的输出，不能只是题目与答案的直接拼接，必须是完整的一句话。

                        示例：

                        题目：股票000554在20210723日期中的收盘价是多少?（小数点保留3位）
                        答案列表：[4.43]
                        股票000554在20210723日期中的收盘价是4.430。

                        题目：20210304日，一级行业为非银金融的股票的成交量合计是多少？取整。
                        答案列表：[2673357760825.0]
                        20210304日，一级行业为非银金融的股票的成交量合计是2673357760825。

                        题目：请帮我查询下，在2019年03月的报告中，报告期基金总申购份额和报告期基金总赎回份额差额最大的一只基金的简称是什么？差额有多少？保留两位小数。
                        答案列表：["000006","西部利得量化成长混合A",608663.9399999976]
                        在2019年03月的报告中，报告期基金总申购份额和报告期基金总赎回份额差额最大的一只基金的简称是西部利得量化成长混合A，差额是608663.94。

                        ###
                        题目：{question}
                        答案列表：{answer_list}
                        ###
                    '''

    # 定义请求的JSON数据
    data = {
        "model": "Qwen-7B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": content
            }
        ],
        "do_sample": True,
        "temperature": 0.1,
        "top_p": 0,
        "n": 1,
        "max_tokens": 1024,
        "stream": False
    }

    # 发送POST请求
    sess = requests.Session()
    response = sess.post(url, json=data, timeout=10 * 60)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应JSON数据
        response_data = response.json()
        # 处理响应数据
        answer = response_data.get('choices')[0].get('message').get('content')

        return answer
    else:
        print(f"请求失败，状态码: {response.status_code}")


template_file_path = '../../answer_template/answer_template.json'
with open(template_file_path, "r", encoding="utf-8") as file:
    template_datas = json.load(file)

answer_file_path = '../sql_get_answer/A_sql_answer_1129.json'
with open(answer_file_path, "r", encoding="utf-8") as file:
    answer_datas = json.load(file)

for obj in answer_datas[597:]:
    id = obj['a_id']
    question = obj['a_question']
    answer_list = obj['a_answer']
    template = template_datas[id]['answer']

    print(question)
    print(template)
    print(answer_list)

    answer = Qwen_post(question, template, answer_list)

    output_file = "A_answer_1202.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"id": id, "question": question, "answer": answer}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')


