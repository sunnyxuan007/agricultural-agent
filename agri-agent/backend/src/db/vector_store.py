# 向量数据库管理模块（可选，因为 load_knowledge.py 中已直接使用 Chroma）
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

def get_vectorstore(persist_dir="./chroma_db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings)