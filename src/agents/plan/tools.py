from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from ...config import Config
from .constants import BUDGET_PROMPT, ITINERARY_PROMPT
from .schemas import BudgetResult, ItineraryResult


@tool
def create_itinerary(destination: str, days: int, interests: str) -> ItineraryResult:
    """Create a travel itinerary for the specified destination and interests."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(ItineraryResult)

    prompt = ITINERARY_PROMPT.format(
        destination=destination, days=days, interests=interests
    )
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result


@tool
def calculate_budget(
    destination: str, days: int, accommodation_type: str = "hotel"
) -> BudgetResult:
    """Calculate estimated budget for the trip."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(BudgetResult)

    prompt = BUDGET_PROMPT.format(
        destination=destination, days=days, accommodation_type=accommodation_type
    )
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result
