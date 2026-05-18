import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


def main():
    # 检查知识库目录
    kb_dir = "data/knowledge"
    if not os.path.exists(kb_dir):
        print(f"错误：知识库目录 {kb_dir} 不存在")
        return

    # 加载所有 markdown 文件
    docs = []
    for filepath in glob.glob(f"{kb_dir}/*.md"):
        loader = TextLoader(filepath, encoding="utf-8")
        docs.extend(loader.load())

    if not docs:
        print("未找到任何 .md 文件，请先添加知识库内容。")
        return

    # 分块
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # 向量化并存储
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="./chroma_db"
    )
    vectorstore.persist()
    print(f"✅ 知识库加载完成！共 {len(chunks)} 个文本块。")


if __name__ == "__main__":
    main()