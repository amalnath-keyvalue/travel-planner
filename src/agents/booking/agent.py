"""Booking agent implementation."""

from langgraph.prebuilt import create_react_agent

from ...config import get_llm_model
from .constants import BOOKING_AGENT_PROMPT
from .tools import search_accommodations, search_flights


def create_booking_agent():
    """Create the booking agent for accommodations and flights."""
    return create_react_agent(
        model=get_llm_model(),
        tools=[search_accommodations, search_flights],
        prompt=BOOKING_AGENT_PROMPT,
        name="booking_agent",
    )
