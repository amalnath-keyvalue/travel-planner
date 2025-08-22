"""Supervisor agent tools."""

from langgraph.graph import MessagesState

from ...config import get_llm_model
from .constants import SUPERVISOR_DECISION_PROMPT
from .schemas import SupervisorDecision


def make_supervisor_decision(user_message: str) -> SupervisorDecision:
    """Let supervisor autonomously decide how to handle the request."""
    llm = get_llm_model().with_structured_output(SupervisorDecision)
    prompt = SUPERVISOR_DECISION_PROMPT.format(user_message=user_message)
    return llm.invoke(prompt)


def should_continue(state: MessagesState) -> str:
    """Determine if workflow should continue or end."""
    messages = state.get("messages", [])
    if not messages:
        return "END"

    last_message = messages[-1]

    if hasattr(last_message, "name") and last_message.name in [
        "search_agent",
        "booking_agent",
        "supervisor",
    ]:
        return "END"

    return "supervisor"
