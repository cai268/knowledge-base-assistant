import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from datetime import datetime,timedelta
from langchain.agents.middleware import SummarizationMiddleware


# 这里指定记忆缓存的位置
connection = sqlite3.connect("./storage/SQlite/checkpoint.db",check_same_thread=False)
checkpointer = SqliteSaver(connection)# 初始化checkpointer
checkpointer.setup()

# 设置记忆id
config = {"configurable":{"thread_id": "thread_1"}}

# 自动清理函数
def clean_thread(thread_id_to_delete):
    """删除特定会话的所有历史"""
    try:
        cursor = connection.cursor()

        # 先查询所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'checkpoint%' OR name LIKE 'channel%' OR name='writes'")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DELETE FROM {table[0]} WHERE thread_id = ?", (thread_id_to_delete,))

        connection.commit()
        print(f"已删除 thread_id: {thread_id_to_delete}")
    except Exception as e:
        print(f"删除失败: {e}")


# 上下文
middleware = SummarizationMiddleware(
    model="deepseek-v4-pro",# 让模型自己给超出的文本进行总结
    trigger=("messages",6),
    keep=("messages",3)
)