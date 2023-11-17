import json
import sqlite3
import pandas as pd

db_path = '../../bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

sql = """SELECT "A股公司行业划分表"."一级行业名称", COUNT("A股公司行业划分表"."股票代码")
FROM "A股公司行业划分表"
WHERE "A股公司行业划分表"."交易日期" = '20201022'
GROUP BY "A股公司行业划分表"."一级行业名称"
ORDER BY COUNT("A股公司行业划分表"."股票代码") DESC
LIMIT 1;"""

result = cursor.execute(sql)
data = cursor.fetchone()

print(data[0])
if data[0] != 0:
    print("right")
else:
    print("wrong")

conn.close()
