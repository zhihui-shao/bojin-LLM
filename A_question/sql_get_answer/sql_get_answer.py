import sqlite3
import json
import pandas as pd

# Replace 'your_database.db' with the path to your actual database file.
db_path = '../../bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

# Construct the SQL query string
file_path = '../sql_finetune/all_right_sql.json'

with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)

    for obj in datas:
        a_id = obj['a_id']
        a_question = obj['a_question']
        sql = obj['sql']
        a_answer = []

        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            a_answer = list(data)
            output_file = "A_sql_answer_1129.json"
            print(a_question)
            print(a_answer)
            obj['a_answer'] = a_answer
            with open(output_file, "a", encoding="utf-8") as output:
                json.dump(obj, output, ensure_ascii=False, indent=4)
                output.write(',' + '\n')
        except Exception as e:
            print(e)


# 关闭数据库连接
conn.close()

