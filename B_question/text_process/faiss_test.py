from sentence_transformers import SentenceTransformer
from text_splitter import ChineseRecursiveTextSplitter
import faiss
import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 读取和切割文本
def read_and_split_text(file_path):
    file_path = os.path.join(folder_path, file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        paragraphs = text_splitter.split_text(text)
    return paragraphs

# 得到embedding
def get_datas_embedding(datas):
    embedding = model.encode(datas)
    return embedding

# 索引的创建
def create_index(paragraphs):
       
    embedding = get_datas_embedding(paragraphs)      
    # embedding = embedding.reshape(1, -1) 
    print(embedding.shape)
    index = faiss.IndexFlatL2(embedding.shape[1])  # 这里必须传入一个向量的维度，创建一个空的索引
    index.add(embedding)   # 把向量数据加入索引
         
    return index

# 数据检索
def data_recall(faiss_index, query, top_k):
    model = SentenceTransformer('moka-ai/m3e-base')
    query_embedding = model.encode([query])
    print(query_embedding.shape)
    Distance, Index = faiss_index.search(query_embedding, top_k)
    return Index

# 创建索引的保存
def faiss_index_save(faiss_index, save_file_location):
    faiss.write_index(faiss_index, save_file_location)

# 索引的加载
def faiss_index_load(faiss_index_save_file_location):
    index = faiss.read_index(faiss_index_save_file_location)
    return index

# 向索引中添加向量
def index_data_add(faiss_index):
    # 获得索引向量的数量
    print(faiss_index.ntotal)
    data = ["小丁的文章太好看了"]
    datas_embedding = get_datas_embedding(data)
    faiss_index.add(datas_embedding)
    print(faiss_index.ntotal)



if __name__ == "__main__":
    
    model = SentenceTransformer('moka-ai/m3e-base')
    
    text_splitter = ChineseRecursiveTextSplitter(
        keep_separator=True,
        is_separator_regex=True,
        chunk_size=600,
        chunk_overlap=60
    )

    folder_path = '../../bs_challenge_financial_14b_dataset/pdf_txt_file'
    file_paths = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
      
    for i, file_path in enumerate(file_paths):
        paragraphs = read_and_split_text(file_path)
        
        faiss_index = create_index(paragraphs)
        new_file_name = file_path.replace(".txt", ".index")        
        save_location = f'./faiss/{new_file_name}'
        faiss_index_save(faiss_index, save_location)
        print(f"第{i}个文档完成了")
        

    # question =  "昇兴集团股份有限公司因租赁厂房存在经营风险的下属企业是什么？"

    # faiss_index = faiss_index_load("./faiss/1af01c24b0957a1ab6d9262b93d7ccf7093f0529.index")
    
    # sim_data_Index = data_recall(faiss_index, question, 3)
    # print(sim_data_Index)
    # print("相似的top3数据是：")
    # for index in sim_data_Index[0]:
    #     print(paragraphs[int(index)] + "\n=================\n")
