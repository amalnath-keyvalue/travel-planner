from langchain.agents import AgentExecutor, create_react_agent

from ...config import Config
from ...constants import REACT_PROMPT
from .tools import calculate_budget, create_itinerary


class PlanAgent:
    def __init__(self):
        self.llm = Config.get_llm()
        self.tools = [create_itinerary, calculate_budget]

        self.agent = create_react_agent(self.llm, self.tools, REACT_PROMPT)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=False
        )

    def process_request(self, request: str):
        return self.agent_executor.invoke({"input": request})
