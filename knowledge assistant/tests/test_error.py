import sys
from pathlib import Path

# 添加项目根目录到路径
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from langchain.messages import HumanMessage
from src.agent import *
from src.tools import *

def test_error():
    test_cases = [{
            "name": "空查询",
            "query": "",
            "expected": ["未找到", "请输入", "不能为空"]
        },
        {
            "name": "超长查询",
            "query": "A" * 10000,
            "expected": ["过长", "截断", "限制"]
        },
        {
            "name": "特殊字符",
            "query": "!@#$%^&*()_+{}|:<>?",
            "expected": []
        },
        {
            "name": "SQL注入",
            "query": "'; DROP TABLE users; --",
            "expected": []
        },
        {
            "name": "Emoji",
            "query": "什么是CPU？🧠💻",
            "expected": []
        }]

    results = {
        "pass" : 0,
        "fail" : 0,
        "details":[]
    }

    for test in test_cases:
        print("=" * 20 + f"查询{test["name"]}" + "=" * 20)
        query = test['query']

        try:
            response = agent.invoke(
                {"messages":[HumanMessage(query)]},
                config
            )

            result = response['messages'][-1].content

            if result is not None:
                print(f"执行成功\n返回值为：{result}")

                error_keyword = any(kw in result for kw in ['error','failed','错误','失败'])
                if error_keyword:
                    print("返回了错误信息(但没崩溃)")
                    results["fail"] += 1
                else:
                    print("返回结果正确，执行成功")
                    results["pass"] += 1
            else:
                print("返回的结果是空值")
                results["fail"] += 1

        except Exception as e:
            print("+++程序破溃+++")
            print(f"崩溃类型{e}")
            results["fail"] += 1
            results["details"].append({
                "name" : test["name"],
                "error" : str(e)
            })

    print("=" * 20 + "测试结果总结" + "=" * 20)
    print(f"成功的次数：{results["pass"]}")
    print(f"失败的次数：{results["fail"]}")
    for detail in results["details"]:
        print(f"{detail["name"]}:{detail["error"]}")

    return results

test_error()
