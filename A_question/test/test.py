import json
import sqlite3
import pandas as pd

db_path = '../../bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

sql = """SELECT "A股票日行情表"."股票代码", MAX(("A股票日行情表"."收盘价(元)" - "A股票日行情表"."昨收盘(元)") / "A股票日行情表"."昨收盘(元)" * 100)
FROM "A股票日行情表", "A股公司行业划分表"
WHERE "A股票日行情表"."股票代码" = "A股公司行业划分表"."股票代码"
AND "A股公司行业划分表"."一级行业名称" = '综合金融';"""

result = cursor.execute(sql)
data = cursor.fetchone()

print(data[0])
print(data)
print(list(data))
if data[0] != 0:
    print("right")
else:
    print("wrong")

conn.close()
