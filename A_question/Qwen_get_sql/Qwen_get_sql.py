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
                        你是一名Mysql数据库开发人员，你精通Mysql数据库的sql代码编写，你需要根据已知的表名、字段名和用户输入的问题编写sql代码。
                        已知表名:
                        A股公司行业划分表 已知字段:[股票代码、交易日期、行业划分标准、一级行业名称、二级行业名称]
                        A股票日行情表 已知字段:[股票代码、交易日、昨收盘(元)、今开盘(元)、最高价(元)、最低价(元)、收盘价(元)、成交量(股)、成交金额(元)]
                        港股票日行情表 已知字段:[股票代码、交易日、昨收盘(元)、今开盘(元)、最高价(元)、最低价(元)、收盘价(元)、成交量(股)、成交金额(元)]
                        基金份额持有人结构 已知字段:[基金代码、基金简称、公告日期、截止日期、机构投资者持有的基金份额、机构投资者持有的基金份额占总份额比例、个人投资者持有的基金份额、个人投资者持有的基金份额占总份额比例、定期报告所属年度、报告类型]
                        基金股票持仓明细 已知字段:[基金代码、基金简称、持仓日期、股票代码、股票名称、数量、市值、市值占基金资产净值比、第N大重仓股、所在证券市场、所属国家(地区)、报告类型]
                        基金规模变动表 已知字段:[基金代码、基金简称、公告日期、截止日期、报告期期初基金总份额、报告期基金总申购份额、报告期基金总赎回份额、报告期期末基金总份额、定期报告所属年度、报告类型]
                        基金基本信息 已知字段:[基金代码、基金全称、基金简称、管理人、托管人、基金类型、成立日期、到期日期、管理费率、托管费率]
                        基金可转债持仓明细 已知字段:[基金代码、基金简称、持仓日期、对应股票代码、债券名称、数量、市值、市值占基金资产净值比、第N大重仓股、所在证券市场、所属国家(地区)、报告类型]
                        基金日行情表 已知字段:[基金代码、交易日期、单位净值、复权单位净值、累计单位净值、资产净值]
                        基金债券持仓明细 已知字段:[基金代码、基金简称、持仓日期、债券类型、债券名称、持债数量、持债市值、持债市值占基金资产净值比、第N大重仓股、所在证券市场、所属国家(地区)、报告类型]
                        
                        注意: sql代码必须是可以执行的，字段名必须是已知字段名，不得新增字段名；表中的日期格式都为YYYYmmdd；只需给出相应的sql语句，不要有任何额外的内容。

                        示例模版：
                        用户输入：请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。
                        SELECT "A股票日行情表"."股票代码", MAX(("A股票日行情表"."收盘价(元)" - "A股票日行情表"."昨收盘(元)") / "A股票日行情表"."昨收盘(元)" * 100)
                        FROM "A股票日行情表", "A股公司行业划分表"
                        WHERE "A股票日行情表"."股票代码" = "A股公司行业划分表"."股票代码"
                        AND "A股公司行业划分表"."一级行业名称" = '综合';
                        用户输入：请帮我查询出20210415日，建筑材料一级行业涨幅超过5%（不包含）的股票数量。
                        SELECT COUNT(*)
                        FROM "A股公司行业划分表", "A股票日行情表"
                        WHERE "A股票日行情表"."交易日" = '20210415'
                        AND "A股公司行业划分表"."一级行业名称" = '建筑材料'
                        AND "A股公司行业划分表"."股票代码" = "A股票日行情表"."股票代码"
                        AND ("A股票日行情表"."收盘价(元)" - "A股票日行情表"."昨收盘(元)") / "A股票日行情表"."昨收盘(元)" * 100 > 5;
                        用户输入：请查询在2021年度，688338股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停
                        SELECT COUNT(*)
                        FROM "A股票日行情表"
                        WHERE "A股票日行情表"."股票代码" = '688338'
                        AND "A股票日行情表"."交易日" > 20210000
                        AND "A股票日行情表"."交易日" < 20220000
                        AND ("A股票日行情表"."收盘价(元)" / "A股票日行情表"."昨收盘(元)" - 1) * 100 >= 9.8
                        
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


file_path = '../../q_classify/A_question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)

for obj in datas:
    id = obj['a_id']
    question = obj['a_question']
    match = False
    answer = Qwen_post(question)
    print(answer)

    output_file = "A_sql.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"a_id": id, "a_question": question, "keywords": answer}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')


