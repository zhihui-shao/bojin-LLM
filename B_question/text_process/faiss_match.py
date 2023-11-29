from text_splitter import ChineseRecursiveTextSplitter
import faiss
import os
import json
import requests
from faiss_test import data_recall,faiss_index_load
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('moka-ai/m3e-base')
from text_splitter import ChineseRecursiveTextSplitter

def Qwen_post(question,match_paragraph):
    
    # 定义API接口的URL
    url = 'http://localhost:8000/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Tongyi-Finance-14B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                        你是文本理解专家，你要根据用户输入，结合文档，给出最合理的回答。
                        要求：仔细阅读文档，找出文档中与用户输入最相关的内容，保证输出语义通顺合理。
                        只需要回答用户输入的问题，不需要解释原因，也不需要回答其他内容。
                        
                        示例：
                        用户输入:东莞勤上光电股份有限公司实际控制人是谁？持有多少股份？
                        文档:['一、股份限制流通及自愿锁定承诺\n本次发行前公司总股本 14,050.00 万股，本次拟发行股票 4,683.50 万
                            股，发\n行后总股本18,733.50万股，上述股份均为流通股。\n公司控股股东东莞勤上集团有限公司、实际控制人李旭亮先生和温琦
                            女士、\n东莞市合盈创业投资有限公司、李淑贤、梁金成、莫群积分别承诺：自公司股票', '三、控股股东及实际控制人的简要情况\n本
                            公司实际控制人为李旭亮先生和温琦女士。李旭亮先生和温琦女士是夫妻\n关系。\n发行人总股本为14,050.00万股，其中李旭亮夫
                            妇通过勤上集团持有4,851.70\n万股股份，', '况\n公司成立以来，独立从事提供照明产品及照明综合解决方案服务及相关业\n务，不存在经营依赖控股股东等情形。在生产经营方面与主要 ']
                        输出:东莞勤上光电股份有限公司实际控制人是李旭亮先生和温琦女士，他们持有4,851.70万股股份。
                        
                        用户输入:浙江开尔新材料股份有限公司的主要原材料有哪些？
                        文档:['\n(b)业主选择的背衬材料。产品所需的配套材料-背衬材料用料对公司制定投\n标价格有较大影响。背衬材料用料分为镀锌板、铝蜂窝材料、硅酸盖 ', 
                            '公即单个客户的销售金额占公司营业收入的比\n重将处于不断下降趋势。\n公司不存在向单个客
                            户销售比例超过销售收入总额 50％或严重依赖少数客\n户的情况。\n（五）主要原材料及能源供应情况\n1、报告期内公司生产
                            成本构成情况\n公司生产所需原材料主要是低碳冷轧\n材料等其他材料占比较小。', '\n（五）主要原材料及能源供应情况\n1、报告期内公司
                            生产成本构成情况\n公司生产所需原材料主要是低碳冷轧钢板和搪瓷釉料，背衬材料、龙骨系统\n材料等其他材料占比较小。
                            报告期内公司生产成本构成情况如下：\n1、报告期内公司生产成本构成情况\n公司生产所需原材料主要是低碳冷轧钢板和搪瓷釉料，
                            背衬材料、龙骨系统\n材料等其他材料占比较小。']
                        输出:浙江开尔新材料股份有限公司的主要原材料有低碳冷轧钢板和搪瓷釉料，背衬材料、龙骨系统材料。
                        
                        用户输入:烟台杰瑞石油服务集团股份有限公司获得过哪些荣誉称号？
                        文档:['业务：油田专用设备制造，油田、矿山设备维修改造及配件销售和海上油田钻\n采平台工程作业服务。\n烟台杰
                            瑞成立于 1999 年 12 月，目前是国家科技部认定的“国家火炬计划重点高新\n技术企业”，曾获“山东省优秀中小企业”、“山东 
                            省成长型中小企业”、 2006年度和2007\n年度“烟台市百强民营企业”等多项荣誉称号。\n公司目前全面推行 HSE(Health 职业健
                            康、Safety 职业安全和 Environment 环保)管\n理体系，并通', '\n一、根据公司2008年2月23日
                            召开的2008年第二次临时股东大会以及2008年12\n月21日召开的2008年第五次临时股东大会决议：公司发行上市前的 
                            滚存利润由上市以\n后的新老股东按照持股比例共同享有。\n二、公司实际控制人孙伟杰、', '转让或者委托他人
                            管理其所持有的烟台杰瑞的股份，也不由烟台杰瑞回购其所持有的股\n份：(1)自烟台杰瑞首次向社会公开发行股票并上市之日 
                            起 36 个月内；(2)自烟台杰瑞\n离职后 6 个月内。']
                        输出:烟台杰瑞石油服务集团股份有限公司获得过“山东省优秀中小企业”、“山东省成长型中小企业”、 2006年度和2007年度“烟台市百强民营企业”等多项荣誉称号。
                                   
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
    chunk_size=600,
    chunk_overlap=60
)
kw_path = '../key2txt/B_kw2txt.json'
with open(kw_path, "r", encoding="utf-8") as file:
    datas = json.load(file)   
    
faiss_folder_path = './faiss'
txt_folder_path = '../../bs_challenge_financial_14b_dataset/pdf_txt_file'

for obj in datas: 
    id = obj['b_id']    
    question = obj['b_question'] 
    keywords = obj["keywords"]
    txt_name = obj['txt_name']       
    print("id:",id)
    if txt_name == "":
        print("================================")
    else:
        if id > 878:
            index_name = txt_name.replace(".txt", ".index") 
            index_path = os.path.join(faiss_folder_path, index_name)
            # print(index_path)
            txt_path = os.path.join(txt_folder_path, txt_name)
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()
                paragraphs = text_splitter.split_text(text)

            faiss_index = faiss_index_load(index_path)
            sim_data_Index = data_recall(faiss_index, question, 3)
            # print(sim_data_Index)
            # print("相似的top3数据是：")
            paragraph = []
            for index in sim_data_Index[0]:
                # print(paragraphs[int(index)])
                paragraph.append(paragraphs[int(index)])    
            # print(paragraph)  
            
            answer = Qwen_post(question,paragraph).strip()
            print(answer)
            jsonl_file_path = '../../answer_template/answer_1124_faiss.jsonl'
            replace_answer(jsonl_file_path, id, answer)
        else:
            print("该问题已经回答过了")