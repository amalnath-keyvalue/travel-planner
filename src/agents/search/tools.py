from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from src.config import Config

from .constants import SEARCH_DESTINATIONS_PROMPT, WEATHER_PROMPT
from .schemas import SearchResult, WeatherResult


@tool
def search_destinations(query: str, budget: float = 1000) -> SearchResult:
    """Search for travel destinations based on query and budget."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(SearchResult)

    prompt = SEARCH_DESTINATIONS_PROMPT.format(query=query, budget=budget)
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result


@tool
def check_weather(destination: str) -> WeatherResult:
    """Check weather for a specific destination."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(WeatherResult)

    prompt = WEATHER_PROMPT.format(destination=destination)
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result
