from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from text_splitter import ChineseRecursiveTextSplitter

m3e_model = SentenceTransformer('moka-ai/m3e-base')

# 初始化 Elasticsearch 客户端
es = Elasticsearch(hosts="http://localhost:9200",request_timeout=3600)

text_splitter = ChineseRecursiveTextSplitter(
    keep_separator=True,
    is_separator_regex=True,
    chunk_size=1500,
    chunk_overlap=150
)

# 读取和切割文本
def read_and_split_text(file_path):
    file_path = os.path.join(folder_path, file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        paragraphs = text_splitter.split_text(text)
    return paragraphs

# 将文本嵌入向量并存储到 Elasticsearch
def index_text_vectors(index_name, file_paths):
    for i, file_path in enumerate(file_paths):
        paragraphs = read_and_split_text(file_path)

        for j, paragraph in enumerate(paragraphs):
            # 转换文本段为嵌入向量
            embedding = m3e_model.encode(paragraph)

            # 存储向量到 Elasticsearch
            doc = {
                'file_id': i,
                'paragraph_id': j,
                'text': paragraph,
                'vector': embedding.tolist(),
            }

            es.index(index=index_name, doc_type='_doc', body=doc)
            
        print(f"完成第{i}个文件")

# 搜索最相似的文本段
def search_similar_text(index_name, question):
    # 转换问题为嵌入向量
    question_embedding = m3e_model.encode(question)

    # 在 Elasticsearch 中执行语义相似度搜索
    query = {
        'query': {
            'script_score': {
                'query': {'match_all': {}},
                'script': {
                    'source': 'cosineSimilarity(params.query_vector, "vector") + 1.0',
                    'params': {'query_vector': question_embedding.tolist()}
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    # 提取最相似的文本段
    hits = result['hits']['hits']
    if hits:
        best_hit = hits[0]['_source']
        return best_hit['file_id'], best_hit['paragraph_id'], best_hit['text']
    else:
        return None

# 主程序
if __name__ == "__main__":
    # 定义索引名称
    index_name = 'text_vectors_index'
    
    import os
    import json
    folder_path = '../../bs_challenge_financial_14b_dataset/pdf_txt'
    file_paths = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 将文本嵌入向量并存储到 Elasticsearch
    # index_text_vectors(index_name, file_paths)

    # 示例问题
    question = "昇兴集团股份有限公司本次发行的拟上市证券交易所是？"

    # 搜索最相似的文本段
    result = search_similar_text(index_name, question)

    if result:
        file_id, paragraph_id, text = result
        print(f"最相似的文本段来自文档 {file_id + 1}，第 {paragraph_id + 1} 段:\n{text}")
    else:
        print("没有找到相似的文本段。")
