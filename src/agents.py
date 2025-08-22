"""Specialized worker agents following LangGraph patterns."""

import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

from .config import get_llm_model
from .tools import (
    calculate_trip_budget,
    create_detailed_itinerary,
    get_weather_forecast,
    search_accommodations,
    search_destinations,
    search_flights,
)

load_dotenv()


def create_search_agent():
    """Create the search agent for destinations and weather."""
    print("🔵 Creating search agent...")
    agent = create_react_agent(
        model=get_llm_model(),
        tools=[search_destinations, get_weather_forecast],
        prompt=(
            "You are a travel search agent specializing in destinations and weather.\n\n"
            "INSTRUCTIONS:\n"
            "- Use your tools to search for destinations and get weather information\n"
            "- Provide detailed recommendations with specific details\n"
            "- Include practical information like costs, best times to visit, and highlights\n"
            "- Be enthusiastic and helpful in your responses\n"
            "- After completing your search, provide a comprehensive summary\n"
            "- DO NOT attempt to do planning, budgeting, or booking tasks"
        ),
        name="search_agent",
    )
    print("🔵 Search agent created")
    return agent


def create_planning_agent():
    """Create the planning agent for itineraries and budgets."""
    print("🔵 Creating planning agent...")
    agent = create_react_agent(
        model=get_llm_model(),
        tools=[create_detailed_itinerary, calculate_trip_budget],
        prompt=(
            "You are a travel planning agent specializing in itineraries and budgets.\n\n"
            "INSTRUCTIONS:\n"
            "- Create detailed day-by-day itineraries with specific activities\n"
            "- Calculate comprehensive budget breakdowns with realistic costs\n"
            "- Consider travel style and preferences in your planning\n"
            "- Provide practical tips and logistics information\n"
            "- Be thorough and detailed in your planning\n"
            "- After completing planning, provide a clear summary\n"
            "- DO NOT attempt to do destination search or booking tasks"
        ),
        name="planning_agent",
    )
    print("🔵 Planning agent created")
    return agent


def create_booking_agent():
    """Create the booking agent for accommodations and flights."""
    print("🔵 Creating booking agent...")
    agent = create_react_agent(
        model=get_llm_model(),
        tools=[search_accommodations, search_flights],
        prompt=(
            "You are a travel booking agent specializing in accommodations and flights.\n\n"
            "INSTRUCTIONS:\n"
            "- Search for accommodation and flight options based on user requirements\n"
            "- Provide detailed comparisons with prices, amenities, and features\n"
            "- Consider budget constraints and preferences\n"
            "- Offer practical booking advice and tips\n"
            "- Present options clearly with pros and cons\n"
            "- After searching, provide clear recommendations\n"
            "- DO NOT attempt to do destination search or itinerary planning"
        ),
        name="booking_agent",
    )
    print("🔵 Booking agent created")
    return agent
