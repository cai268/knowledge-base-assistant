# 私有知识库助手

这是一个基于 LangChain、LangGraph 和 DeepSeek 大模型构建的智能知识库笔记助手。它能够读取学习笔记，利用大模型能力回答问题，同时具备记忆功能和置信度评估机制。

## ✨ 功能特点

- **智能问答**：检索知识库笔记，通过自然语言给出答复，而非简单的关键词搜索
- **本地私有知识库**：通过 ChromaDB 和 Embedding 模型，检索向量化后的知识库
- **置信度评估**：基于向量检索的相似度、一致性和分数分布，自动评估回答的可信度
- **脏数据自动清理**：自动过滤文档中的页码、联系方式、邮箱等无效信息，提高检索质量
- **智能重试机制**：当置信度不足时自动重试，确保回答质量
- **记忆功能**：使用 SQLite 持久化存储对话记忆，支持多轮对话
- **上下文窗口管理**：利用 Middleware 设置上下文窗口，提高响应效率
- **自动清理**：程序结束后自动删除本次记忆，避免磁盘占用过大

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.13 |
| 框架 | LangChain / LangGraph |
| 向量数据库 | ChromaDB |
| 记忆存储 | SQLite |
| 向量化模型 | HuggingFace Embeddings (BGE) |
| LLM 模型 | DeepSeek API |
| 项目管理 | UV |
| 测试框架 | Pytest |

## 📁 项目结构
```
.
├── src/ # 源代码
│ ├── init.py
│ ├── main.py # 程序入口
│ ├── agent.py # Agent 创建与配置
│ ├── tools.py # 工具定义（知识检索）
│ ├── confidence.py # 置信度计算模块
│ ├── clean.py # 脏数据清理模块
│ ├── config.py # 配置管理
│ └── memory.py # 记忆管理
│
├── tests/ # 测试代码
│ ├── init.py
│ ├── conftest.py # Pytest 共享配置
│ ├── test_confidence.py # 置信度单元测试
│ └── test_clean.py # 脏数据清理测试
│
├── data/ # 知识库数据
│ └── 计算机知识.txt
│ └──local_doc_db/ # 向量数据库存储
│ 
├── scripts/ # 脚本工具
│ └── 数据向量化.py # 数据向量化脚本
│
├── .env # 环境变量配置
├── .gitignore # Git 忽略文件
├── pyproject.toml # 项目配置
├── uv.lock # UV 锁文件
└── README.md # 项目说明
```
text

## 🚀 快速启动

### 环境配置

- Python 3.13+
- DeepSeek API Key（或其他兼容的 API）

### 安装依赖

使用 UV（推荐）：
```bash
uv sync
或使用 pip：

bash
pip install -r requirements.txt
依赖列表（pyproject.toml）：

toml
dependencies = [
    "langchain>=1.3.10",
    "langchain-chroma>=1.1.0",
    "langchain-community>=0.4.2",
    "langchain-deepseek>=1.1.0",
    "langgraph>=1.2.6",
    "langgraph-checkpoint-sqlite>=3.1.0",
    "langchain-huggingface>=1.2.2",
    "sentence-transformers>=5.7.0",
    "python-dotenv>=1.2.2",
    "pypdf>=4.0.0",
    "pytest>=8.0.0",
]
```
### 配置环境变量
创建 .env 文件并配置：

env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
EMBEDDING_MODEL=BAAI/bge-base-zh-v1.5


bash
## 知识库存储
python scripts/数据向量化.py
说明：

默认向量化 ./data/ 目录下的文档

向量库存储在 ./local_doc_db/

如需自定义，修改脚本中的文件路径即可

### 运行 Agent
python -m src.main
启动后输入 exit 可退出程序。

##  运行测试
bash
### 运行所有测试
uv run pytest tests/

### 运行特定测试
python -m src.test_confidence.py

