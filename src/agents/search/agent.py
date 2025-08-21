from langchain.agents import AgentExecutor, create_react_agent

from ...config import Config
from ...constants import REACT_CHAT_PROMPT
from .tools import check_weather, search_destinations


class SearchAgent:
    def __init__(self):
        self.llm = Config.get_llm()
        self.tools = [search_destinations, check_weather]

        self.agent = create_react_agent(self.llm, self.tools, REACT_CHAT_PROMPT)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=False
        )

    def process_request(self, request: str):
        return self.agent_executor.invoke({"input": request})
