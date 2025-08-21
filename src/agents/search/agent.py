from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.config import Config

from .constants import SEARCH_AGENT_SYSTEM
from .tools import check_weather, search_destinations


class SearchAgent:
    def __init__(self):
        self.llm = Config.get_llm()
        self.tools = [search_destinations, check_weather]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SEARCH_AGENT_SYSTEM),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=False
        )

    def process_request(self, request: str):
        return self.agent_executor.invoke({"input": request})
