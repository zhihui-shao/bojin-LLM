from question_cls import questions_classify
from extract_company_names import extract_company_names
from text_questions import Qwen_get_companys,company_name2txt
from jieba_match import text_answer

def main():
    
    #问题分类，A类为SQL查询题，B类为文本理解题
    questions_classify()
    
    #利用Qwen将txt文档和公司名称对应起来
    extract_company_names()
    
    #用Qwen提取问题中的公司名称
    Qwen_get_companys()
    
    #将问题和公司名称和txt文档对应起来
    company_name2txt()
    
    #文档切分，匹配，获取Qwen回答
    text_answer()
    
    
    
    
    
if __name__ == "__main__":
    main()