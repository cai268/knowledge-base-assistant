import sys
from pathlib import Path

# 添加项目根目录到路径
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from langchain.messages import HumanMessage
from src.agent import *
from src.tools import *


# ========================信任度检测========================
def test_confidant():
    # 实验用户问题
    test_query = "什么是计算机，计算机发展了多少年"

    # 模拟查询
    print("=" * 25 + "模拟查询" + "=" * 25)
    mock_results = [# 模拟索引
        (type('Doc', (), {'page_content': 'CPU是中央处理器'})(), 0.85),
        (type('Doc', (), {'page_content': 'CPU负责执行指令'})(), 0.72),
        (type('Doc', (), {'page_content': 'CPU是计算机核心'})(), 0.61)
]

    confidant = confidance(mock_results)

    if 0 <= confidant <= 1:
        print(f"模拟信任度结果{confidant * 100}%,模拟结果合理\n")
    else:
        print("模拟结果不在合理范围内\n")

    # 检测空数据
    empty_confidant = confidance([])
    if empty_confidant == 0.0:
        print("空查询信任度0%,结果正确\n")
    else:
        print(f"空查询信任度应为0%,但真实结果为{empty_confidant * 100}%\n")

# 真实查询
    print("=" * 25 + "真实查询" + "=" * 25)
    response = agent.invoke({"messages":[HumanMessage(test_query)]},config)
    print(f"AI:{response['messages'][-1].content}\n")

# 运行测试函数
test_confidant()