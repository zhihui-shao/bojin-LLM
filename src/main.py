from question_cls import questions_classify
from extract_company_names import extract_company_names
from text_questions import Qwen_get_companys,company_name2txt
from jieba_match import text_answer
from question_match_sql import get_sql
from sql_get_answer import sql_get_answer
from Qwen_sql_fill_answer import get_final_answer
from get_answer import merge_file, json2jsonl
from jsonl2json import jsonl_to_json


def main():

    # 转化文件格式
    jsonl_to_json()
    
    # 问题分类，A类为SQL查询题，B类为文本理解题
    questions_classify()
    
    # 利用Qwen将txt文档和公司名称对应起来
    extract_company_names()
    
    # 用Qwen提取问题中的公司名称
    Qwen_get_companys()
    
    # 将问题和公司名称和txt文档对应起来
    company_name2txt()
    
    # 文档切分，匹配，获取Qwen回答
    text_answer()
    
    # 正则匹配获取问题sql
    get_sql()

    # 运行sql得到结果
    sql_get_answer()

    # 提示Qwen，结合题目和查询结果生成答案
    get_final_answer()

    # 合并文件并生成jsonl
    merge_file()
    json2jsonl()
    
    
if __name__ == "__main__":
    main()
