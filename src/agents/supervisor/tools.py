"""Supervisor agent tools."""

from langchain_core.tools import tool


@tool
def delegate_to_search_agent(user_request: str) -> str:
    """Delegate request to search agent for weather, location info, or external data needs."""
    return "DELEGATED_TO_SEARCH"


@tool
def delegate_to_booking_agent(user_request: str) -> str:
    """Delegate request to booking agent for hotels, flights, reservations, or booking confirmations."""
    return "DELEGATED_TO_BOOKING"
