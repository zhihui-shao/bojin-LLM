from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer



# 创建一个 PyPDFLoader Class 实例，输入为待加载的pdf文档路径
loader = PyPDFLoader("../../bs_challenge_financial_14b_dataset/pdf/0b46f7a2d67b5b59ad67cafffa0e12a9f0837790.PDF")

# 调用 PyPDFLoader Class 的函数 load对pdf文件进行加载
pages = loader.load()

print(len(pages))

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=150, length_function=len)

splits = text_splitter.split_documents(pages)
print(splits)


