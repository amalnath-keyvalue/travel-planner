from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from ...config import Config
from .constants import ACCOMMODATION_PROMPT, BOOKING_PROMPT
from .schemas import AccommodationResult, BookingResult


@tool
def find_accommodation(
    destination: str, budget: float, accommodation_type: str = "hotel"
) -> AccommodationResult:
    """Find accommodation options using LLM."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(AccommodationResult)

    prompt = ACCOMMODATION_PROMPT.format(
        destination=destination, budget=budget, accommodation_type=accommodation_type
    )
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result


@tool
def confirm_booking(
    destination: str, accommodation: str, dates: str, price: float
) -> BookingResult:
    """Confirm a booking using LLM."""
    llm = Config.get_llm()
    llm_with_structured_output = llm.with_structured_output(BookingResult)

    prompt = BOOKING_PROMPT.format(
        destination=destination, accommodation=accommodation, dates=dates, price=price
    )
    result = llm_with_structured_output.invoke([HumanMessage(content=prompt)])
    return result
