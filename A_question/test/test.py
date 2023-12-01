# coding=utf-8
# 用LLM提取问题中的公司名称和关键字
import json
import requests


def Qwen_post(question, template, answer_list):
    # 定义API接口的URL
    url = 'http://172.31.233.206:8000/v1/chat/completions'

    content = f'''
                        你是一位有名的答案填空专家，给你一个题目和答案列表，你需要根据题目所要求的数据格式，如小数点位数、百分比、是否取整等，参考示例，将答案列表结合问题，生成语义通顺且符合题目要求的答案。
                        请注意，你所给出的结果必须来自给定的输入，不要有任何额外的输出，不能只是题目与答案的直接拼接。

                        示例：
                        题目：请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                        答案列表：["300773",43.99038461538461]
                        在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是300773，涨跌幅是43.99%。

                        题目：我想知道股票300819在申万行业分类下的二级行业是什么？用最新的数据。
                        答案列表：["纺织制造"]
                        300819在申万行业分类下的二级行业是纺织制造。

                        题目：我想知道安信稳健回报6个月持有期混合A基金在20211231的年报(含半年报)中，其可转债持仓占比最大的是哪个行业？用中信一级行业来统计。
                        答案列表：["苏银转债",0.0843]
                        在20211231的年报(含半年报)中，安信稳健回报6个月持有期混合A基金可转债持仓占比最大的行业是苏银转债。

                        题目：股票000554在20210723日期中的收盘价是多少?（小数点保留3位）
                        答案列表：[4.43]
                        股票000554在20210723日期中的收盘价是4.430。

                        题目：20210304日，一级行业为非银金融的股票的成交量合计是多少？取整。
                        答案列表：[2673357760825.0]
                        20210304日，一级行业为非银金融的股票的成交量合计是2673357760825。

                        题目：请查询：在20210611，属于申万二级一般零售行业的A股股票，它们的平均成交金额是多少？小数点后保留不超过5位。
                        答案列表：[2673357760825.0]
                        20210304日，一级行业为非银金融的股票的成交量合计是2673357760825。

                        题目：请帮我查询下，在2019年03月的报告中，报告期基金总申购份额和报告期基金总赎回份额差额最大的一只基金的简称是什么？差额有多少？保留两位小数。
                        答案列表：["000006","西部利得量化成长混合A",608663.9399999976]
                        在2019年03月的报告中，报告期基金总申购份额和报告期基金总赎回份额差额最大的一只基金的简称是西部利得量化成长混合A，差额是608663.94。

                        题目：请帮我计算，代码为603937的股票，2020年一年持有的年化收益率有多少？百分数请保留两位小数。年化收益率定义为：（（有记录的一年的最终收盘价-有记录的一年的年初当天开盘价）/有记录的一年的当天开盘价）* 100%。
                        答案列表：[71.52103559870552]
                        代码为603937的股票，2020年一年持有的年化收益率是71.52%。

                        ###
                        题目：{question}
                        答案列表：{answer_list}
                        ###
                    '''

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": content
            }
        ],
        "do_sample": True,
        "temperature": 0,
        "top_p": 0,
        "n": 1,
        "max_tokens": 8192,
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

for obj in answer_datas[312:]:
    id = obj['a_id']
    question = obj['a_question']
    answer_list = obj['a_answer']
    template = template_datas[id]['answer']

    print(question)
    print(template)
    print(answer_list)

    answer = Qwen_post(question, template, answer_list)

    output_file = "A_answer_1201.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"id": id, "question": question, "answer": answer}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')


