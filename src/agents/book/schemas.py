from typing import List

from pydantic import BaseModel, Field


class AccommodationResult(BaseModel):
    destination: str = Field(description="Destination name")
    options: List[str] = Field(description="List of accommodation options")
    prices: List[float] = Field(description="Prices for each option")
    locations: List[str] = Field(description="Location details for each option")
    recommendations: List[str] = Field(description="Why each option is recommended")


class BookingResult(BaseModel):
    destination: str = Field(description="Destination name")
    accommodation: str = Field(description="Accommodation name")
    confirmation_code: str = Field(description="Booking confirmation code")
    total_price: float = Field(description="Total booking price")
    next_steps: List[str] = Field(description="What the user should do next")
