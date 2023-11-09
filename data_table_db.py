import sqlite3
import pandas as pd

# Replace 'your_database.db' with the path to your actual database file.
db_path = './bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'
# Replace 'your_table_name' with the actual table name from which you want to retrieve data.
table_name = 'A股公司行业划分表'
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

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

# Construct the SQL query string
query = f"SELECT COUNT(*) FROM {table_name} WHERE 一级行业名称='轻工制造' AND 交易日期 = '20201231'"


# 使用pandas读取数据
df = pd.read_sql_query(query, conn)

# 显示前10条数据，包括表头信息
print(df)

# 关闭数据库连接
conn.close()

