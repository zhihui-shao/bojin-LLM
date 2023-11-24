from langchain.document_loaders import PyPDFLoader

# 加载 PDF
loaders_chinese = [
    # 故意添加重复文档，使数据混乱
    PyPDFLoader("../../bs_challenge_financial_14b_dataset/pdf/0b46f7a2d67b5b59ad67cafffa0e12a9f0837790.PDF")
]
docs = []
for loader in loaders_chinese:
    docs.extend(loader.load())
    
# 分割文本
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,  # 每个文本块的大小。这意味着每次切分文本时，会尽量使每个块包含 1500 个字符。
    chunk_overlap = 150  # 每个文本块之间的重叠部分。
)

splits = text_splitter.split_documents(docs)

print(len(splits))

from sentence_transformers import SentenceTransformer
 
model = SentenceTransformer('moka-ai/m3e-base')
 
#Our sentences we like to encode
sentences = [
    '''武汉力源信息技术股份有限公司
Wuhan P&S Information Technology Co., Ltd.
武汉市洪山区珞瑜路 424 号洪山创业大       
首次公开发行股票并在创业板上市
招股意向书
保荐机构(主承销商)'''
]
 
#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)
 
#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

import chromadb
chroma_client = chromadb.PersistentClient(path="/chroma/")
collection = chroma_client.create_collection(name="my_collection")
