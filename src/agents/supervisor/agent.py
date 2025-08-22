"""Supervisor agent implementation."""

from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import END, MessagesState

from .constants import SupervisorAction
from .tools import make_supervisor_decision


def supervisor_node(state: MessagesState) -> dict:
    """Autonomous supervisor that decides how to handle requests."""
    last_message = state["messages"][-1]

    # If last message is from an agent, conversation is complete
    if hasattr(last_message, "name") and last_message.name in [
        "search_agent",
        "booking_agent",
    ]:
        return {"next": "END"}

    # Let supervisor decide autonomously
    decision = make_supervisor_decision(last_message.content)

    if decision.action == SupervisorAction.REJECT:
        rejection_msg = SystemMessage(
            content="I'm a travel planning assistant. Please ask me about destinations, trip planning, or booking travel arrangements."
        )
        return {
            "messages": state["messages"] + [rejection_msg],
            "next": "END",
        }

    elif decision.action == SupervisorAction.HANDLE_MYSELF:
        return {
            "messages": state["messages"]
            + [AIMessage(content=decision.response, name="supervisor")],
            "next": "END",
        }

    elif decision.action == SupervisorAction.DELEGATE_TO_SEARCH:
        return {"next": "search_agent"}

    elif decision.action == SupervisorAction.DELEGATE_TO_BOOKING:
        return {"next": "booking_agent"}

    else:
        return {"next": "search_agent"}


def route_to_agent(
    state: MessagesState,
) -> Literal["search_agent", "booking_agent", END]:
    """Route to the appropriate agent based on supervisor's decision."""
    if "next" in state:
        next_choice = state["next"]
        return END if next_choice == "END" else next_choice
    return "search_agent"
