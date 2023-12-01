import jieba 
import json
import string
from text_splitter import ChineseRecursiveTextSplitter
import os
from collections import Counter

text_splitter = ChineseRecursiveTextSplitter(
    keep_separator=True,
    is_separator_regex=True,
    chunk_size=800,
    chunk_overlap=80
)
file_path = '../../q_classify/B_question.json'
with open(file_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   

for obj in datas: 
    id = obj['b_id']     
    question = obj['b_question']
    seg_list = jieba.cut(question, cut_all=False)
    print(id)
    jieba_list = "/".join(seg_list).split("/")
    custom_words = ["多少", "哪些", "怎样", "何时", "什么", "是否"]
    # print(jieba_list)
    result_list = [item for item in jieba_list if item not in string.punctuation and len(item) > 1 and item not in custom_words]

    print(result_list)






# import fool
# import os

# # 分词
# text = "我来到北京清华大学"
# print(fool.cut(text))