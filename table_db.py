import sqlite3
import pandas as pd
# 替换此处的'database.db'为你的.db文件路径
database_path = './bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'

# 连接到SQLite数据库
conn = sqlite3.connect(database_path)
cursor = conn.cursor()
table_names = [
            '基金基本信息',
            '基金股票持仓明细',
            '基金债券持仓明细',
            '基金可转债持仓明细',
            '基金日行情表',
            'A股票日行情表',
            '港股票日行情表',
            'A股公司行业划分表',
            '基金规模变动表',
            '基金份额持有人结构',
]
# 创建一个 Cursor 对象并调用其 execute() 方法来执行 SQL 命令

for table_name in table_names:
    # 执行查询
    query = f"SELECT * FROM {table_name} LIMIT 10"
    # query = f"SELECT DISTINCT 一级行业名称 FROM {table_name}"
    # 使用pandas读取数据
    df = pd.read_sql_query(query, conn)
    # 显示前10条数据，包括表头信息
    print(df)
    print('====================================================')

# 关闭数据库连接
conn.close()


# 总共有10张表
# 基金基本信息
# 基金股票持仓明细
# 基金债券持仓明细
# 基金可转债持仓明细
# 基金日行情表
# A股票日行情表
# 港股票日行情表
# A股公司行业划分表
# 基金规模变动表
# 基金份额持有人结构