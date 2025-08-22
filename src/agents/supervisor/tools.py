"""Supervisor agent tools."""

from typing import Annotated

from langchain_core.tools import tool
from langgraph.graph import MessagesState
from langgraph.types import Command, Send


@tool
def transfer_to_search_agent(
    task_description: Annotated[
        str,
        "Description of what the search agent should do, including all of the relevant context.",
    ],
    state: Annotated[MessagesState, "InjectedState"],
) -> Command:
    """Assign task to search agent for weather, location info, or external data needs."""
    task_description_message = {"role": "user", "content": task_description}
    agent_input = {**state, "messages": [task_description_message]}
    return Command(
        goto=[Send("search_agent", agent_input)],
        graph=Command.PARENT,
    )


@tool
def transfer_to_booking_agent(
    task_description: Annotated[
        str,
        "Description of what the booking agent should do, including all of the relevant context.",
    ],
    state: Annotated[MessagesState, "InjectedState"],
) -> Command:
    """Assign task to booking agent for hotels, flights, reservations, or booking confirmations."""
    task_description_message = {"role": "user", "content": task_description}
    agent_input = {**state, "messages": [task_description_message]}
    return Command(
        goto=[Send("booking_agent", agent_input)],
        graph=Command.PARENT,
    )
