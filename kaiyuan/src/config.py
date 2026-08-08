from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 加载参数
load_dotenv()

# prompt
system_prompt = '''
# 身份
- 你是一个日常学习助手,用户将笔记分割成向量库发给你,你来帮用户查找并总结相应的知识点
- 同时，当用户询问非知识库的问题时,你可用依靠自己来答复

# 指令
- 必须按照JSON格式输出,不要加任何markdown格式
'''

# 加载向量库
# 初始化embedding模型
emd = HuggingFaceEmbeddings(
    model_name = "D:/AI_tool/embedding_models/BAAI/models/BAAI--bge-base-zh-v1.5/snapshots/master",
    model_kwargs={"device": "cpu"}
)

# 加载数据库
vector_db = Chroma(
    persist_directory = "./local_doc_db",
    embedding_function=emd
)