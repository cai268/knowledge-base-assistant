import sys
from pathlib import Path

# 添加项目根目录到路径
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from src.tools import *

# ========================脏数据处理========================
sample_1 = """
邮购电话：（010）88254888
CPU是中央处理器
邮箱：zlts@phei.com.cn
"""

sample_2 = """
第291页
网络层负责数据包转发
① 这是脚注内容
"""

sample_3 = """
QQ交流群：123456789
QQ:12345567
操作系统是管理计算机硬件和软件的程序
版权所有 翻印必究
"""

sample_4 = """
联系及邮购电话：（010）88254888
计算机网络（第7版）谢希仁
质量投诉请发邮件至 zlts@phei.com.cn
本书咨询联系方式：QQ 9616328
第3章 网络体系结构
"""
def test_clean_function():
    # 整合脏数据样本
    sample = [sample_1,sample_2,sample_3,sample_4]
    # 开始清理脏数据
    for i,dirty in enumerate(sample,1):
        print("=" * 20 + f"进行第{i}段清理" + "=" * 20)

        clear_sample = clear_data(dirty)

        print(f"清理完后的样本：{clear_sample}")

# 运行测试脏数据处理
test_clean_function()