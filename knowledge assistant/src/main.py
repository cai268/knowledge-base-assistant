from .agent import *
from langchain.messages import HumanMessage

if __name__ == "__main__":
    print("学习聊天助手已启动，输入exit退出程序")
    while True:
        user_query = input("输入")
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