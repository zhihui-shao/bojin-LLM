import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
os.environ["OPENAI_API_KEY"] = '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'

llm = OpenAI(temperature=0)

sqlite_db_path ='../../bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db'
db = SQLDatabase.from_uri(f"sqlite:///{sqlite_db_path}")
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
result = db_chain.run("请帮我查询出20210415日，建筑材料一级行业涨幅超过5%（不包含）的股票数量。")
print(result)
print(type(result))
print(result.SQLQuery)
# 导入数据库报错：openai.error.InvalidRequestError:
# This model's maximum context length is 4097 tokens,
# however you requested 6617 tokens (6361 in your prompt; 256 for the completion).
# Please reduce your prompt; or completion length.
