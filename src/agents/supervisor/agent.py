"""Supervisor agent implementation."""

from langgraph.prebuilt import create_react_agent

from ...config import get_llm_model
from .constants import SUPERVISOR_AGENT_PROMPT
from .tools import transfer_to_booking_agent, transfer_to_search_agent


def create_supervisor_agent():
    """Create the supervisor agent with routing tools."""
    return create_react_agent(
        model=get_llm_model(),
        tools=[transfer_to_search_agent, transfer_to_booking_agent],
        prompt=SUPERVISOR_AGENT_PROMPT,
        name="supervisor",
    )
