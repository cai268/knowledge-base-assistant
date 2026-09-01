# 学习资料查询tool
from pydantic import BaseModel,Field
from typing import Literal
from langchain_core.tools import tool
from .config import *
from .clean import *
from .confidence import *

@tool
def Get_Notes(user_query:str):
    '''
    - user_query:用户提问的问题
    - 每次用户提问时都检查一下回复的信任度，若信任度过低，则让用户更换询问方式
    - 每次回答都先给出信任度后在做回答，确保尽可能高的信任度
    '''
    # 检索
    try:
        if user_query is None:
            print("请输入您的问题")
        # 检索并计算信任度
        count = 1
        best_confidant = 0.0
        best_respond = None
        while count < 4:
            print(f"正在进行第{count}次检索...")
            respond = vector_db.similarity_search_with_score(user_query,k=2)
            # 检查检索结果
            if not respond or len(respond) == 0:
                return "未找到相关信息，请换个方式提问"
            confidant = confidance(respond)# 计算

            if confidant > best_confidant:# 找到最佳回答
                best_confidant = confidant
                best_respond = respond
            count += 1
        # 处理脏数据
        raw_content = best_respond[0][0].page_content
        clear_respond = clear_data(raw_content)
        # clear_respond = 1
    
        if best_confidant >= 0.7:
            result= f"置信度是{best_confidant * 100}%,可以相信,内容是{clear_respond}"
        elif best_confidant >= 0.4:
            result= f"置信度是{best_confidant * 100}%,置信度较低,请谨慎相信此答案,内容是{clear_respond}"
        else:
            result= f"置信度是{best_confidant * 100}%,无法找到答案，请换个询问方式"

        return result
    except Exception as e:
        return f"检索失败:{e}"
    