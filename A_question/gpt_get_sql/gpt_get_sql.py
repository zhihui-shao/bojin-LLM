# 用LLM将问题转化为SQL语句
import json
import requests
import re
import openai
import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = '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'


def gpt_post(question):

    llm = ChatOpenAI()

    template_string = """
                        你是一名Mysql数据库开发人员，你精通Mysql数据库的sql代码编写，你需要根据已知的表名、字段名和用户输入的问题编写sql代码。
                        已知表名:
                        A股公司行业划分表 已知字段:[股票代码,交易日期,行业划分标准,一级行业名称,二级行业名称] 数据示例:[000065,20190115,中信行业分类,建筑,建筑施工Ⅱ]
                        A股票日行情表 已知字段:[股票代码,交易日,昨收盘(元),今开盘(元),最高价(元),最低价(元),收盘价(元),成交量(股),成交金额(元)] 数据示例:[603665,20190131,28.32,27.5,28.09,25.49,27.28,1757953,48247793]
                        港股票日行情表 已知字段:[股票代码,交易日,昨收盘(元),今开盘(元),最高价(元),最低价(元),收盘价(元),成交量(股),成交金额(元)] 数据示例:[47 HK,20190125,0.162,0.16,0.164,0.16,0.163,68000,10908]
                        基金份额持有人结构 已知字段:[基金代码,基金简称,公告日期,截止日期,机构投资者持有的基金份额,机构投资者持有的基金份额占总份额比例,个人投资者持有的基金份额,个人投资者持有的基金份额占总份额比例,定期报告所属年度,报告类型] 数据示例:[000006,西部利得量化成长混合A,2019-08-24 00:00:00,2019-06-30 00:00:00,10000600,7.24,128087037.15,92.76,2019,中期报告]
                        基金股票持仓明细 已知字段:[基金代码,基金简称,持仓日期,股票代码,股票名称,数量,市值,市值占基金资产净值比,第N大重仓股,所在证券市场,所属国家(地区),报告类型] 数据示例:[007484,信澳核心科技混合A,20201231,600563,法拉电子,151369,16279735.95,0.0257,4,上海证券交易所,中华人民共和国,季报]
                        基金规模变动表 已知字段:[基金代码,基金简称,公告日期,截止日期,报告期期初基金总份额,报告期基金总申购份额,报告期基金总赎回份额,报告期期末基金总份额,定期报告所属年度,报告类型] 数据示例:[000028,华富安鑫债券,2019-04-20 00:00:00,2019-03-31 00:00:00,344550555.65,1811778.99,18997687.33,327364647.31,2019,基金定期报告]
                        基金基本信息 已知字段:[基金代码,基金全称,基金简称,管理人,托管人,基金类型,成立日期,到期日期,管理费率,托管费率] 数据示例:[000006,西部利得量化成长混合型发起式证券投资基金A类,西部利得量化成长混合A,西部利得基金管理有限公司,中国农业银行股份有限公司,混合型,20190319,30001231,1.2%,0.1%]
                        基金可转债持仓明细 已知字段:[基金代码,基金简称,持仓日期,对应股票代码,债券名称,数量,市值,市值占基金资产净值比,第N大重仓股,所在证券市场,所属国家(地区),报告类型] 数据示例:[006650,招商安庆债券,20191231,300568,星源转债,1815,225989.4,0.0013,36,深圳证券交易所,中华人民共和国,季报]
                        基金日行情表 已知字段:[基金代码,交易日期,单位净值,复权单位净值,累计单位净值,资产净值] 数据示例:[007120,20210120,2.162,2.162,2.162,3282338328.05]
                        基金债券持仓明细 已知字段:[基金代码、基金简称、持仓日期、债券类型、债券名称、持债数量、持债市值、持债市值占基金资产净值比、第N大重仓股、所在证券市场、所属国家(地区)、报告类型] 数据示例:[010005,鹏扬现金通利货币E,20210331,超短期融资券,21华能水电SCP002,200000,20000180.24,0.0253,9,银行间市场,中华人民共和国,季报]

                        注意: sql代码必须是可以执行的，字段名必须是已知字段名，不得新增字段名；只需给出相应的sql语句，不要有任何额外的内容。

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
                        AND ("A股票日行情表"."收盘价(元)" / "A股票日行情表"."昨收盘(元)" - 1) * 100 >= 9.8;
                        
                        ###
                        用户输入：{question}
                        ###
                    """

    prompt_template = ChatPromptTemplate.from_template(template_string)

    customer_messages = prompt_template.format_messages(question=question)

    customer_response = llm(customer_messages)
    return customer_response.content


file_path = '../../q_classify/A_question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)

for obj in datas:
    id = obj['a_id']
    print(id)
    question = obj['a_question']
    answer = gpt_post(question)
    print(answer)

    output_file = "A_sql_4.json"  # 每次循环迭代都将结果追加到JSON文件
    with open(output_file, "a", encoding="utf-8") as output:
        json.dump({"a_id": id, "a_question": question, "sql": answer}, output, ensure_ascii=False, indent=4)
        output.write(',' + '\n')
