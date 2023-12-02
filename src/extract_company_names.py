# 将80个txt文档的文件名与公司名称对应起来
import requests
import os
import json
import re

def Qwen_post(t):
    
    # 定义API接口的URL
    url = 'http://172.31.233.204:8001/v1/chat/completions'

    # 定义请求的JSON数据
    data = {
        "model": "Qwen-7B-Chat",
        "messages": [
            {
                "role": 'user',
                "content": f'''
                    你是一个能精准提取信息的AI。
                    我会给你一篇招股说明书的部分内容，请输出此招股说明书的主体是哪家公司，若无法查询到，则输出无。\n
                    
                    示例模板：
                    招股说明书：[不對因本公告全部或任何部份內容而產生或因依
                        而引致的任何損失承擔任何責任。
                        Bank of Qingdao Co., Ltd.*
                        青 島 銀 行 股 份 有 限 公 司*
                        （於中華人民共和國註冊成立的股份有限公司）
                        （H股股份代號：3866）
                        （優先股股份代號：4611）
                        本公告乃根據《香港聯合交易所有限公司證券上市規則》第13.10B條刊登。
                        該公告已於深圳證券交易所網站刊登，茲載列如下，僅供參閱。
                        特此公]
                    输出：青岛银行股份有限公司
                    
                    招股说明书：[背事实真相的虚假记载、误导性陈述，或在披露信息时发生重大
                            遗漏，导致发行人不符合法律规定的发行条件，造成投资者直接经济损失的，  
                            将先行赔偿投资者损失。
                            发行人会计师声明：本所承诺：因本所为安徽黄山胶囊股份有限公司首次      
                            公开发行股票并上市制作、出具的文件有虚假记载、误导性陈述或者重大遗漏，
                            给投资者造成损失的，将依法赔偿投资者损失，如能证明本所没有过错的除外。
                            发行人律师承诺：如本所在本次发行工作期间未勤勉尽责]
                    输出：安徽黄山胶囊股份有限公司
     
                    招股说明书:[于有权部门处罚和认定事实
                        之日起30 日内启动回购措施。若本公司未能履行回购股份承诺的，本公司承诺
                        将暂停行使表决权，并将当期及以后各期获得的全部分红赠予金石资源，直至承
                        诺履行完毕。
                        若金石资源集团股份有限公司招股意向书有虚假记载、误导性陈述或者重大
                        遗漏，致使投资者在证券交易中遭受损失的，本公司将依法赔偿投资者损失。”
                        公司实际控制人王锦华承诺：“若金石资源招股意向书有虚假记载、误导性
                        陈述或者重大遗漏，]
                    输出：金石资源集团股份有限公司
                    
                    招股说明书：[保荐人暨主承销商
                            中信建投证券有限责任公司
                            北京市朝阳区安立路 66 号 4 号楼
                            北京七星华创电子股份有限公司
                            （一）发行股票类型： 人民币普通股（A股）
                            （二）预计发行量： 1,656万股
                            （三）每股面值： 人民币1元
                            （四）每股发行价格： 待询价后确定
                            （五）预计发行日期： 2010年3月3日
                            （六）拟上]
                    输出：北京七星华创电子股份有限公司
                    
                    
                    请按照上述示例模板，分析招股说明书属于哪家公司，只输出公司名，保证以“股份有限公司”或“科技有限公司”结尾                    
                    招股说明书：{t}
                    输出：
                '''
            }
        ],
        "do_sample": True,
        "temperature": 0,
        "top_p": 0,
        "n": 1,
        "max_tokens": 2048,
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
        
def find_companies(text):
    pattern = re.compile(r'股份有限公司|科技有限公司')
    matches = pattern.finditer(text)

    for match in matches:
        start_index = match.start()
        if start_index >= 2 and (text[start_index-2:start_index] == "证券" or text[start_index-2:start_index] == "金融"):
            continue

        prefix_start = max(0, start_index - 100)
        suffix_end = min(len(text), start_index + len(match.group()) + 100)

        company_info = text[prefix_start:suffix_end]  # 调整提取的范围
        return company_info


def extract_company_names():
    # 指定目录路径
    directory_path = "../bs_challenge_financial_14b_dataset/pdf_txt_file"

    # 获取目录中所有的txt文件名
    txt_files = [f for f in sorted(os.listdir(directory_path)) if f.endswith('.txt')]
    json_list = []
    # 将每个文件名存为一条json数据
    for file_name in txt_files:
        if file_name == '54d148902b889679830174597830f0d0f22c1073.txt':
            company_name = "上海派能能源科技股份有限公司"
        elif file_name == '756171248e278806a56171d59c6519a38eac9012.txt':
            company_name = "确成硅化学股份有限公司"
        elif file_name == '91b4426b075560a1a45247f9cfa9fa73d56c945c.txt':
            company_name = "广州中海达卫星导航技术股份有限公司"
        elif file_name == 'a244b6ed9da7411f804e62b82a8fdfc015dff284.txt':
            company_name = "惠州光弘科技股份有限公司"
        elif file_name == 'afa8c5a4a91c3ecf7bd38a1c1f09b8a68e472909.txt':
            company_name = "山东海看网络科技有限公司"
        elif file_name == 'e1e8e0551703f4a1f2873755ef46210b0889c5cd.txt':
            company_name = "读者出版传媒股份有限公司"
        elif file_name == 'e774a06e6b4db734424f7d9181b9515a08bea6cc.txt':
            company_name = "中钢集团安徽天源科技股份有限公司"
        elif file_name == 'f30bfe8be4ad535d348d74f80eaef8d93b3c8ac5.txt':
            company_name = "上海维科精密模塑股份有限公司"
        elif file_name == 'bec898d3079074d88f8bdb34d7e07f072cfca695.txt':
            company_name = "中国神华能源股份有限公司"
        elif file_name == 'e6ff749bb533a47173aaca91fe5d44080d9d37b3.txt':
            company_name = "广东银禧科技股份有限公司"
        elif file_name == '07d29cd67ca8e0fc932e05178db1fcdca1cee937.txt':
            company_name = "青岛银行股份有限公司"
        else:
            file_path = os.path.join(directory_path, file_name)
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                company_text = find_companies(content)
                print(company_text)
        
                company_name = Qwen_post(company_text)
                print(company_name)
        
        json_list.append({"file_name": file_name,"company_name":company_name})

    # 将json数据写入文件
    with open('extract_company_names.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_list, json_file, ensure_ascii=False,indent=4)

