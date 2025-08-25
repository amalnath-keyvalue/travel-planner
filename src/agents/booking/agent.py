"""Booking agent implementation."""

from langgraph.prebuilt import create_react_agent

from ...config import get_llm_model
from ...utils import debug_hook, human_in_the_loop
from .constants import BOOKING_AGENT_PROMPT
from .tools import (
    confirm_accommodation_booking,
    confirm_flight_booking,
    search_accommodations,
    search_flights,
)


def post_model_hook(state):
    """Post-model hook for the booking agent."""
    debug_hook(state, "BOOKING_POST")
    return human_in_the_loop(
        state, ["confirm_accommodation_booking", "confirm_flight_booking"]
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
        pre_model_hook=lambda state: debug_hook(state, "BOOKING_PRE"),
        version="v2",
        post_model_hook=post_model_hook,
    )
