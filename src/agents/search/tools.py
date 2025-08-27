"""Search agent tools for external API calls and data retrieval."""

import random

from langchain_core.tools import tool

from .schemas import LocationInfo, WeatherInfo


@tool
def get_weather_forecast(destination: str) -> WeatherInfo:
    """Get current weather forecast for a destination.

    Args:
        destination: The destination city or location to get weather for

    Returns:
        WeatherInfo object containing temperature range, conditions, rainfall level, and best time to visit

    Raises:
        ValueError: If destination is empty or whitespace

    Example:
        get_weather_forecast("Paris")
    """
    if not destination or destination.strip() == "":
        raise ValueError("Destination cannot be empty")

    print(f"get_weather_forecast: destination={destination}")

    conditions = ["sunny", "partly cloudy", "light rain", "overcast"]
    rainfall_levels = ["low", "medium", "high"]

    return WeatherInfo(
        destination=destination,
        temperature_range=f"{random.randint(15, 25)}-{random.randint(26, 35)}°C",
        condition=random.choice(conditions),
        rainfall_level=random.choice(rainfall_levels),
        best_time_to_visit="Agent will provide specific recommendations based on destination analysis",
    )


@tool
def get_location_info(destination: str) -> LocationInfo:
    """Get basic location information for a destination.

    Args:
        destination: The destination city or location to get information for

    Returns:
        LocationInfo object containing country, timezone, currency, language, and visa requirements

    Raises:
        ValueError: If destination is empty or whitespace

    Example:
        get_location_info("Tokyo")
    """
    if not destination or destination.strip() == "":
        raise ValueError("Destination cannot be empty")

    print(f"get_location_info: destination={destination}")

    return LocationInfo(
        destination=destination,
        country="Demo Country",
        timezone="UTC+0",
        currency="USD",
        language="English",
        visa_required=random.choice([True, False]),
    )
