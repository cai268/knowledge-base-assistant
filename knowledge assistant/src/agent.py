from langchain.agents import create_agent
from .config import *
from .memory import *
from .tools import *

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=system_prompt,
    checkpointer=checkpointer,
    middleware=[middleware],
    tools=[Get_Notes]
)