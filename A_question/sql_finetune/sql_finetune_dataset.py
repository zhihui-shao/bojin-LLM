import os
import openai
import json
import re

openai.api_type = "azure"
openai.api_base = "https://lechuang.openai.azure.com"
openai.api_key = "bc709d6234e04a80ab2d744eb2434086"
openai.api_version = "2023-05-15"
deployment_name = 'lechuang-gpt-35-bak'


def post(question, sql):
    # 定义API接口的URL
    url = 'http://172.31.233.206:8000/v1/chat/completions'

    content = f'''
                    你是一名专业的Mysql数据库开发人员，你精通Mysql数据库的sql代码编写，现在你需要根据已知的题目和相应的sql语句为例，修改问题给出的条件（如日期等）和对应的sql，来生成新的题目和sql语句。
                    请注意，你只需要给出新的题目和sql语句，不需要有任何额外的输出。
                    
                    示例：
                    题目：请帮我计算，在20200521，申万行业分类划分的一级行业为采掘行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                    sql语句：SELECT \"A股票日行情表\".\"股票代码\", MAX((\"A股票日行情表\".\"收盘价(元)\" - \"A股票日行情表\".\"昨收盘(元)\") / \"A股票日行情表\".\"昨收盘(元)\" * 100)\nFROM \"A股票日行情表\", \"A股公司行业划分表\"\nWHERE \"A股票日行情表\".\"股票代码\" = \"A股公司行业划分表\".\"股票代码\"\nAND \"A股票日行情表\".\"交易日\" = '20200521'\nAND \"A股公司行业划分表\".\"行业划分标准\" = '申万行业分类'\nAND \"A股公司行业划分表\".\"一级行业名称\" = '采掘';
                    新题目：请帮我计算，在20200805，中信行业分类划分的一级行业为机械行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                    新sql语句：SELECT \"A股票日行情表\".\"股票代码\", MAX((\"A股票日行情表\".\"收盘价(元)\" - \"A股票日行情表\".\"昨收盘(元)\") / \"A股票日行情表\".\"昨收盘(元)\" * 100)\nFROM \"A股票日行情表\", \"A股公司行业划分表\"\nWHERE \"A股票日行情表\".\"股票代码\" = \"A股公司行业划分表\".\"股票代码\"\nAND \"A股票日行情表\".\"交易日\" = '20200805'\nAND \"A股公司行业划分表\".\"行业划分标准\" = '中信行业分类'\nAND \"A股公司行业划分表\".\"一级行业名称\" = '机械';
                    
                    题目：请查询在2019年度，603078股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停
                    sql语句：SELECT COUNT(*)\nFROM \"A股票日行情表\"\nWHERE \"A股票日行情表\".\"股票代码\" = '603078'\nAND \"A股票日行情表\".\"交易日\" > 20190000\nAND \"A股票日行情表\".\"交易日\" < 20200000\nAND (\"A股票日行情表\".\"收盘价(元)\" / \"A股票日行情表\".\"昨收盘(元)\" - 1) * 100 >= 9.8;
                    新题目：请查询在2020年度，503378股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停
                    新sql语句：SELECT COUNT(*)\nFROM \"A股票日行情表\"\nWHERE \"A股票日行情表\".\"股票代码\" = '503378'\nAND \"A股票日行情表\".\"交易日\" > 20200000\nAND \"A股票日行情表\".\"交易日\" < 20210000\nAND (\"A股票日行情表\".\"收盘价(元)\" / \"A股票日行情表\".\"昨收盘(元)\" - 1) * 100 >= 9.8;
                    
                    题目：广发稳健增长C基金在20200930的季报里，前三大持仓占比的债券名称是什么?
                    sql语句：SELECT \"债券名称\" \nFROM \"基金债券持仓明细\" \nWHERE \"基金简称\" = '广发稳健增长C' \nAND \"持仓日期\" = '20200930' \nAND \"报告类型\" = '季报'\nORDER BY \"持债市值占基金资产净值比\" DESC \nLIMIT 3;
                    新题目：汕头一达通C基金在20190630的季报里，前三大持仓占比的债券名称是什么?
                    新sql语句：SELECT \"债券名称\" \nFROM \"基金债券持仓明细\" \nWHERE \"基金简称\" = '汕头一达通C' \nAND \"持仓日期\" = '20190630' \nAND \"报告类型\" = '季报'\nORDER BY \"持债市值占基金资产净值比\" DESC \nLIMIT 3;
                    
                    ###
                    题目：{question}
                    sql语句：{sql}
                    新题目：
                    新sql语句：
                    ###
                '''

    try:
        response = openai.ChatCompletion.create(
            engine="lechuang-gpt-35-bak",  # engine = "deployment_name".
            messages=[
                {"role": "user", "content": content}
            ],
            timeout=5 * 60
        )

        # print(response)
        text = response['choices'][0]['message']['content']
        print(text)
        return text
    except Exception as e:
        print("error", str(e))


source_sql = './all_right_sql.json'
with open(source_sql, "r", encoding="utf-8") as file:
    source_datas = json.load(file)

for obj in source_datas[351:]:
    a_id = obj['a_id']
    question = obj['a_question']
    sql = obj['sql']
    output_file = "finetune_sql.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"question": question, "answer": sql}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')

    for i in range(0, 2):
        text = post(question, sql)
        if "新sql语句：" in text and "新题目：" in text:
            str_list = text.split("新sql语句：")
            new_question = str_list[0].strip("新题目：")
            new_sql = str_list[1]
            output_file = "finetune_sql.json"  # 每次循环迭代都将结果追加到JSON文件
            with open(output_file, "a", encoding="utf-8") as output:
                json.dump({"question": new_question, "answer": new_sql}, output, ensure_ascii=False, indent=4)
                output.write(',' + '\n')
        else:
            continue



