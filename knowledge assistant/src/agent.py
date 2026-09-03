# src/agent.py
from langchain.agents import create_agent
from .memory import *
from .tools import *
from .config import *


agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    checkpointer=checkpointer,
    middleware=[middleware],
    tools=[Get_Notes]
)