"""Supervisor agent constants and prompts."""

from enum import Enum


class SupervisorAction(str, Enum):
    """Supervisor action types."""

    DELEGATE_TO_SEARCH = "delegate_to_search"
    DELEGATE_TO_BOOKING = "delegate_to_booking"
    HANDLE_MYSELF = "handle_myself"
    REJECT = "reject"


SUPERVISOR_DECISION_PROMPT = """You are a travel planning supervisor. Analyze this request and decide how to handle it:

Request: "{user_message}"

You can:
- delegate_to_search: for weather, location info, external data needs
- delegate_to_booking: for hotel, flight, reservation needs  
- handle_myself: for itinerary planning, budgeting, general travel advice
- reject: if not travel-related

If you choose 'handle_myself', provide a complete response in the response field. 
Otherwise, leave response empty and explain your delegation reasoning."""
