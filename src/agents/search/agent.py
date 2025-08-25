"""Search agent implementation."""

from langgraph.prebuilt import create_react_agent

from ...config import get_llm_model
from ...utils import debug_hook
from .constants import SEARCH_AGENT_PROMPT
from .tools import get_location_info, get_weather_forecast


def create_search_agent():
    """Create the search agent for destinations and weather."""
    return create_react_agent(
        model=get_llm_model(),
        tools=[get_weather_forecast, get_location_info],
        prompt=SEARCH_AGENT_PROMPT,
        name="search_agent",
        pre_model_hook=lambda state: debug_hook(state, "SEARCH_PRE"),
        post_model_hook=lambda state: debug_hook(state, "SEARCH_POST"),
    )
