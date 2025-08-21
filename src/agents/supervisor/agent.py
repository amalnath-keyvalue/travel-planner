from langchain.agents import AgentExecutor, create_tool_calling_agent

from ...config import Config
from ...constants import REACT_CHAT_PROMPT
from .tools import select_agent


class SupervisorAgent:
    def __init__(self):
        self.llm = Config.get_llm()
        self.tools = [select_agent]

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=REACT_CHAT_PROMPT,
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=False
        )

    def process_request(self, request: str):
        return self.agent_executor.invoke({"input": request})
