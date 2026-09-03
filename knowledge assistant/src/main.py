from .agent import *
from .config import *
from langchain.messages import HumanMessage
import os


if __name__ == "__main__":
    print("学习聊天助手已启动，输入exit退出程序")
    enquire_count = 0
    while True:
        enquire_count += 1
        print("=" * 40 + f"第{enquire_count}段对话" + "=" * 40)
        user_query = input("输入(exit退出程序):")
        print(f"user:{user_query}\n")

        if user_query.strip().lower() == "exit":
            print("程序退出")
            clean_thread("thread_1")# 删除本次的记忆
            break

        # 回复
        agent_response = agent.invoke({
            "messages":[HumanMessage(user_query)]},
            config
            )
        print(f"AI:{agent_response['messages'][-1].content}\n") 