# 学习资料查询tool
from pydantic import BaseModel,Field
from typing import Literal
from langchain_core.tools import tool
from .config import *

class NoteInput(BaseModel):
    user_query:str = Field(description="用户提问的问题")

@tool
def Get_Notes(user_query:str):
    '''
    - 用户提问有关计算机的知识时来获取相关的笔记
    user_query:用户有关计算机的问题
    '''
    # 检索
    test_res = vector_db.similarity_search(user_query, k=2)
    
    if test_res:
        result = f"这个问题的答案是{test_res}"
    else:
        result = "未查询到信息"

    return result
    