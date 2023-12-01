from text_splitter import ChineseRecursiveTextSplitter
import os
from collections import Counter
import json
import re
import requests
import jieba 
import string


def read_and_split_text(file_path):
    folder_path = '../../bs_challenge_financial_14b_dataset/pdf_txt_file'
    file_path = os.path.join(folder_path, file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        paragraphs = text_splitter.split_text(text)
    return paragraphs

def count_keywords(paragraph, keywords):
    # 计算一个段落中包含的关键字个数，但只计算一次
    return sum(1 for keyword in set(keywords) if keyword in paragraph)

def get_top_paragraphs(paragraphs, keywords, top_n=3):
    # 创建一个计数器，用于存储每个段落中关键字的出现次数
    paragraph_counts = Counter()

    # 遍历每个段落，更新计数器
    for paragraph in paragraphs:
        keyword_count = count_keywords(paragraph, keywords)
        paragraph_counts[paragraph] = keyword_count

    # 获取出现关键字最多的前top_n个段落
    top_paragraphs = paragraph_counts.most_common(top_n)
    return top_paragraphs


def Qwen_post(question,match_paragraph):
    
    # 定义API接口的URL
    url = 'http://172.31.233.206:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                        你是文本理解专家，你要根据用户输入的问题，结合文档的内容，给出合理的回答。
                        要求：仔细阅读文档，找出文档中与问题相关的内容，进行总结，然后给出回答。回答必须和文档相关，保证语义通顺合理。
                        只需要回答用户输入的问题即可，不需要解释原因，也不需要回答其他内容。
                        
                        示例模板：
                        用户输入:东莞勤上光电股份有限公司实际控制人是谁？持有多少股份？
                        文档:['一、股份限制流通及自愿锁定承诺\n本次发行前公司总股本 14,050.00 万股，本次拟发行股票 4,683.50 万
                            股，发\n行后总股本18,733.50万股，上述股份均为流通股。\n公司控股股东东莞勤上集团有限公司、实际控制人李旭亮先生和温琦
                            女士、\n东莞市合盈创业投资有限公司、李淑贤、梁金成、莫群积分别承诺：自公司股票', '三、控股股东及实际控制人的简要情况\n本
                            公司实际控制人为李旭亮先生和温琦女士。李旭亮先生和温琦女士是夫妻\n关系。\n发行人总股本为14,050.00万股，其中李旭亮夫
                            妇通过勤上集团持有4,851.70\n万股股份，', '况\n公司成立以来，独立从事提供照明产品及照明综合解决方案服务及相关业\n务，不存在经营依赖控股股东等情形。在生产经营方面与主要 ']
                        输出:东莞勤上光电股份有限公司实际控制人是李旭亮先生和温琦女士，他们持有4,851.70万股股份。

                        用户输入:烟台杰瑞石油服务集团股份有限公司获得过哪些荣誉称号？
                        文档:['业务：油田专用设备制造，油田、矿山设备维修改造及配件销售和海上油田钻\n采平台工程作业服务。\n烟台杰
                            瑞成立于 1999 年 12 月，目前是国家科技部认定的“国家火炬计划重点高新\n技术企业”，曾获“山东省优秀中小企业”、“山东 
                            省成长型中小企业”、 2006年度和2007\n年度“烟台市百强民营企业”等多项荣誉称号。\n公司目前全面推行 HSE(Health 职业健
                            康、Safety 职业安全和 Environment 环保)管\n理体系，并通', '\n一、根据公司2008年2月23日
                            召开的2008年第二次临时股东大会以及2008年12\n月21日召开的2008年第五次临时股东大会决议：公司发行上市前的 
                            滚存利润由上市以\n后的新老股东按照持股比例共同享有。\n二、公司实际控制人孙伟杰、', '转让或者委托他人
                            管理其所持有的烟台杰瑞的股份，也不由烟台杰瑞回购其所持有的股\n份：(1)自烟台杰瑞首次向社会公开发行股票并上市之日 
                            起 36 个月内；(2)自烟台杰瑞\n离职后 6 个月内。']
                        输出:烟台杰瑞石油服务集团股份有限公司获得过“山东省优秀中小企业”、“山东省成长型中小企业”、 2006年度和2007年度“烟台市百强民营企业”荣誉称号。
                           
                        请按照上述示例模板，      
                        #####
                        用户输入:{question}
                        文档:{match_paragraph}
                        输出:    
                        #####
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0.1,
        "top_p": 0,
        "n": 1,
        "max_tokens": 8192,
        "stream": False
    }
    # 发送POST请求
    response = requests.post(url, json=data)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应JSON数据
        response_data = response.json()
        # 处理响应数据
        answer = response_data.get('choices')[0].get('message').get('content')
            
        return answer
    else:
        print(f"请求失败，状态码: {response.status_code}")

    
def replace_answer(jsonl_file, id_to_replace, new_answer):
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        data = json.loads(line)
        if data["id"] == id_to_replace:
            data["answer"] = new_answer
            lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
            break

    with open(jsonl_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)
  
  
        
text_splitter = ChineseRecursiveTextSplitter(
    keep_separator=True,
    is_separator_regex=True,
    chunk_size=800,
    chunk_overlap=80
)

kw_path = '../key2txt/c2txt_1201.json'
with open(kw_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   

for obj in datas: 
    id = obj['b_id']    
    question = obj['b_question'] 
    company_name = obj['company_name']
    txt_name = obj['txt_name']       
    print("id:",id)
    if txt_name == "":
        print("================================")
    else:
        if company_name in question:
            dealt_question = question.replace(company_name, '')
        else:
            dealt_question = question
        print(question)
        print(dealt_question)
        seg_list = jieba.cut(dealt_question, cut_all=False)
        jieba_list = "/".join(seg_list).split("/")
        custom_words = ["多少", "哪些", "怎样", "何时", "什么", "是否","哪个","为什么"]
        # print(jieba_list)
        keywords_list = [item for item in jieba_list if item not in string.punctuation and len(item) > 1 and item not in custom_words]
        

        keywords_list = [word for word in keywords_list if not re.search(r'有限公司', word)]
        print(keywords_list)
        paragraphs = read_and_split_text(txt_name)
        
        top_paragraphs = get_top_paragraphs(paragraphs, keywords_list, top_n=3)
        # 打印结果
        # for paragraph, count in top_paragraphs:
        #     print(f"Paragraph: {paragraph}\nKeyword Count: {count}\n")

        match_paragraph = [item[0] for item in top_paragraphs]
        # print(match_paragraph)
        
    
        answer = Qwen_post(question,match_paragraph).strip()
        print(answer)
        jsonl_file_path = '../../answer_template/answer_1128_kw.jsonl'
        replace_answer(jsonl_file_path, id, answer)
    

            
        
        
        
        


            
        