from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from ...config import Config
from ...state import SupervisorOutput
from .constants import SUPERVISOR_AGENT_SYSTEM, SUPERVISOR_SELECTION_PROMPT


@tool
def select_agent(query: str) -> SupervisorOutput:
    """Select the appropriate agent based on the user query."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(SupervisorOutput)

    messages = [
        SystemMessage(content=SUPERVISOR_AGENT_SYSTEM),
        HumanMessage(content=SUPERVISOR_SELECTION_PROMPT.format(query=query)),
    ]

    return llm_with_structured_output.invoke(messages)
