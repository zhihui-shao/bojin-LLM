from sentence_transformers import SentenceTransformer
import chromadb
from text_splitter import ChineseRecursiveTextSplitter
import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter



model = SentenceTransformer('moka-ai/m3e-base')
text_splitter = ChineseRecursiveTextSplitter(
    keep_separator=True,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50
)

chroma_client = chromadb.PersistentClient(path="./chroma/")

folder_path = '../../bs_challenge_financial_14b_dataset/pdf_txt'
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
print(len(files))

for num, file_name in enumerate(files):
    print(file_name)
    file_path = os.path.join(folder_path, file_name)
    # 打开文件
    with open(file_path, 'r',encoding='utf-8') as file:
        content = file.read()
        
    with open('../key2txt/B_kw2txt.json', 'r',encoding='utf-8') as kw_file:
        datas = json.load(kw_file)
    
    for obj in datas:
        if file_name == obj["txt_name"]:
            company_name = obj["company_name"]
            break
        else:
            company_name = f"{num}"
            
    print(company_name)
    # chroma_client = chromadb.PersistentClient(path=f"./chroma_{company_name}/")
    collection = chroma_client.create_collection(name= 'txt')

    chunks = text_splitter.split_text(content)
    # print(len(chunks))
    embeddings_list = []
    documents_list = []
    metadatas_list = []
    ids_list = []
    for i,chunk in enumerate(chunks):
        embeddings = model.encode(chunk)
        # print(embeddings)
        embeddings_list.append(embeddings)
        documents_list.append(chunk)
        metadatas_list.append({"source": company_name })
        ids_list.append(f"{i}")
        
collection.add(
    embeddings= embeddings_list,
    documents=documents_list,
    metadatas=metadatas_list,
    ids= ids_list
)
    
print(f"第{num}个文件已加载到向量数据库中")


# query_texts= "昇兴集团股份有限公司本次发行的拟上市证券交易所是？"
# query_embeddings = model.encode(query_texts)
# results = collection.query(
#     query_embeddings =  query_embeddings,
#     n_results=3,
#     include = [ "documents" ]
# )

# print(results)
