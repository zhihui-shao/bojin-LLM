import json
import sqlite3
import pandas as pd

db_path = '../../bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

file_path = '../gpt_get_sql/A_sql_3.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)

    for obj in datas:
        id = obj['a_id']
        question = obj['a_question']
        sql = obj['sql']

        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            # 执行成功，返回值大于0
            if data[0] != 0:
                output_file = "A_gpt_right_sql_1.json"  # 每次循环迭代都将结果追加到JSON文件，全对
                with open(output_file, "a", encoding="utf-8") as output:
                    json.dump({"a_id": id, "a_question": question, "sql": sql}, output, ensure_ascii=False, indent=4)
                    output.write(',' + '\n')
            else:
                output_file = "A_gpt_half_sql_1.json"  # 每次循环迭代都将结果追加到JSON文件，可以执行但是结果为0
                with open(output_file, "a", encoding="utf-8") as output:
                    json.dump({"a_id": id, "a_question": question, "sql": sql}, output, ensure_ascii=False, indent=4)
                    output.write(',' + '\n')
        except Exception as e:
            output_file = "A_gpt_wrong_sql_1.json"  # 每次循环迭代都将结果追加到JSON文件，无法执行
            with open(output_file, "a", encoding="utf-8") as output:
                json.dump({"a_id": id, "a_question": question, "sql": sql}, output, ensure_ascii=False, indent=4)
                output.write(',' + '\n')

# 关闭数据库连接
cursor.close()
conn.close()

