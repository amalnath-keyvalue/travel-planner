"""Booking agent implementation."""

from langgraph.prebuilt import create_react_agent

from ...config import get_llm_model
from ...utils import debug_hook
from .constants import BOOKING_AGENT_PROMPT
from .tools import (
    confirm_accommodation_booking,
    confirm_flight_booking,
    search_accommodations,
    search_flights,
)


def create_booking_agent():
    """Create the booking agent for accommodations and flights."""
    return create_react_agent(
        model=get_llm_model(),
        tools=[
            search_accommodations,
            search_flights,
            confirm_accommodation_booking,
            confirm_flight_booking,
        ],
        prompt=BOOKING_AGENT_PROMPT,
        name="booking_agent",
        pre_model_hook=lambda event: debug_hook(event, "BOOKING_PRE"),
        post_model_hook=lambda event: debug_hook(event, "BOOKING_POST"),
    )
