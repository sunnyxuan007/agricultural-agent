from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.tools import tool

embedding = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding)

@tool
def search_knowledge(query: str) -> str:
    """
    从农业知识库中检索相关内容。
    """
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "未找到相关知识。"
    return "\n".join([doc.page_content for doc in results])