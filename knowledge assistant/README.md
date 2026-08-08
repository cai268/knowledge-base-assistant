# 私有知识库助手
这是一个基于langchain和langgragh基于deepseek大模型构建的知识库笔记助手。它能够读取学习我们日常的笔记，可以利用大模型能力回复我们的问题，同时具备一定的记忆功能。

## 功能特点
- 智能答复：它检索知识库笔记并不是简单的关键词搜索，而是能够学习我们的笔记知识并通过自然语言给出答复。
- 本地私有知识库：通过chroma和embedding模型，能够检索向量化后的"./local_doc_db"知识库。
- 记忆功能与自动清理：agent具有记忆功能，且记忆存放在SQlite列表里（硬盘），并且每当程序结束后，都会自动删除本次的记忆文件，避免磁盘占用过大。同时还利 用middleware设置了上下文窗口，提高响应效率。
- 工具调用：能够通过检索工具获取知识库中的相关信息。

## 技术栈
- python 3.13
- langchian/langgragh
- 向量数据库(chromaDB)
- 记忆存储(SQlite)
- 向量化模型embedding
- LLM模型deepseek

## 启动

### 环境配置
- 需要python3.13
- 需要deepseek api(可根据自己用哪个模型选择api)

### 安装依赖
我这里使用的是uv项目管理可以直接：
```bash
uv sync
```
若你不是使用uv：
依赖列表在pyproject.toml文件里
```toml

[project]
name = "kaiyuan"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "ipywidgets>=8.1.8",
    "langchain>=1.3.10",
    "langchain-chroma>=1.1.0",
    "langchain-community>=0.4.2",
    "langchain-deepseek>=1.1.0",
    "langchain-openai>=1.3.2",
    "langchain-qwq>=0.3.5",
    "langchain-text-splitters>=1.1.2",
    "langgraph>=1.2.6",
    "langgraph-checkpoint-sqlite>=3.1.0",
    "notebook>=7.6.0",
    "openai>=2.43.0",
    "python-dotenv>=1.2.2",
    "pypdf>=4.0.0",
    "sentence-transformers>=5.7.0",
    "langchain-huggingface>=1.2.2",
    "datetime>=6.0",
]

[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true

```

### 配置环境变量
在.env文件里面配置你使用大模型的api

### 初始化数据库
在运行agent之前，必须先初始化数据库，可运行文件：
```bash
python 数据向量化.py
```
其中我默认的向量化数据导包存放位置在"./local_doc_db"里面，可自行更改。
同时若想要向量化你的知识库，只需要在data文件夹添加对应的文本，然后在"数据向量化.py"文件里更改build_doc_kb("./data/你的文件")的路径即可。

### 运行agent
在终端运行：
```bash
python -m src.main
```
启动后，可输出exit退出agent

## 项目结构
.
├── date/
│   └── 计算机知识.txt
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── main.py
│   ├── memory.py
│   └── tools.py
├── .env
├── .python-version
├── 数据向量化.py
├── pyproject.toml
├── uv.lock
└── README.md
