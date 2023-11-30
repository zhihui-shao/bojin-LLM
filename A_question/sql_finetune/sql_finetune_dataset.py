import os
import openai
import json

openai.api_type = "azure"
openai.api_base = "https://lechuang.openai.azure.com"
openai.api_key = "bc709d6234e04a80ab2d744eb2434086"
openai.api_version = "2023-05-15"
deployment_name = 'lechuang-gpt-35-bak'


def post(question, sql):
    # 定义API接口的URL
    url = 'http://172.31.233.206:8000/v1/chat/completions'

    content = f'''
                    你是一名专业的Mysql数据库开发人员，你精通Mysql数据库的sql代码编写，现在你需要根据已知的题目和相应的sql语句为例，来生成新的题目和sql语句。
                    请注意，你只需要给出新的题目和sql语句，不需要有任何额外的输出。
                    
                    示例：
                    题目：请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                    sql语句：SELECT \"A股票日行情表\".\"股票代码\", MAX((\"A股票日行情表\".\"收盘价(元)\" - \"A股票日行情表\".\"昨收盘(元)\") / \"A股票日行情表\".\"昨收盘(元)\" * 100)\nFROM \"A股票日行情表\", \"A股公司行业划分表\"\nWHERE \"A股票日行情表\".\"股票代码\" = \"A股公司行业划分表\".\"股票代码\"\nAND \"A股公司行业划分表\".\"一级行业名称\" = '综合金融';
                    新题目：请帮我计算，在20200805，申万行业分类划分的一级行业为机械行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                    新sql语句：SELECT \"A股票日行情表\".\"股票代码\", MAX((\"A股票日行情表\".\"收盘价(元)\" - \"A股票日行情表\".\"昨收盘(元)\") / \"A股票日行情表\".\"昨收盘(元)\" * 100)\nFROM \"A股票日行情表\", \"A股公司行业划分表\"\nWHERE \"A股票日行情表\".\"股票代码\" = \"A股公司行业划分表\".\"股票代码\"\nAND \"A股公司行业划分表\".\"一级行业名称\" = '综合金融';
                    
                    题目：请查询在2019年度，603078股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停
                    sql语句：SELECT COUNT(*)\nFROM \"A股票日行情表\"\nWHERE \"A股票日行情表\".\"股票代码\" = '603078'\nAND \"A股票日行情表\".\"交易日\" > 20190000\nAND \"A股票日行情表\".\"交易日\" < 20200000\nAND (\"A股票日行情表\".\"收盘价(元)\" / \"A股票日行情表\".\"昨收盘(元)\" - 1) * 100 >= 9.8;
                    新题目：请查询在2020年度，503378股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停
                    新sql语句：SELECT COUNT(*)\nFROM \"A股票日行情表\"\nWHERE \"A股票日行情表\".\"股票代码\" = '603078'\nAND \"A股票日行情表\".\"交易日\" > 20190000\nAND \"A股票日行情表\".\"交易日\" < 20200000\nAND (\"A股票日行情表\".\"收盘价(元)\" / \"A股票日行情表\".\"昨收盘(元)\" - 1) * 100 >= 9.8;
                    
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
            token=8000,
            timeout=5 * 60
        )

        # print(response)
        text = response['choices'][0]['message']['content']
        print(text)
    except Exception:
        print("error")


# source_sql = './all_right_sql.json'
# with open(source_sql, "r", encoding="utf-8") as file:
#     gpt_right_sql_datas = json.load(file)





