from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "./local_doc_db"

def build_doc_kb(file_path: str):
    # 加载文档
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    raw_docs = loader.load()

    # 文本切片设置
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(raw_docs)

    # 本地embedding模型
    # 由于这里用的是本地embeddign模型，所以模型地址看embedding位置
    emb = HuggingFaceEmbeddings(model_name="D:/AI_tool/embedding_models/BAAI/models/BAAI--bge-base-zh-v1.5/snapshots/master",
                                model_kwargs={"device": "cpu"})

    # 向量化并存到本地
    Chroma.from_documents(
        documents=chunks,
        embedding=emb,
        persist_directory=PERSIST_DIR
    )
    print("知识库构建完成")


if __name__ == "__main__":
    build_doc_kb("./date/你的文件")