"""Booking agent schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Accommodation(BaseModel):
    """Accommodation option."""
    name: str
    type: str
    price_per_night: int
    rating: float
    amenities: List[str]
    pros: str
    cons: str


class AccommodationSearch(BaseModel):
    """Accommodation search results."""
    destination: str
    check_in: str
    check_out: str
    guests: int
    options: List[Accommodation]
    booking_tips: List[str]


class Flight(BaseModel):
    """Flight option."""
    airline: str
    price: int
    rating: float
    departure_time: str
    duration: str
    stops: int
    travel_class: str


class FlightSearch(BaseModel):
    """Flight search results."""
    route: str
    departure_date: str
    return_date: Optional[str]
    is_roundtrip: bool
    options: List[Flight]
    booking_tips: List[str]


class BookingResponse(BaseModel):
    """Booking agent response."""
    accommodations: Optional[AccommodationSearch] = None
    flights: Optional[FlightSearch] = None
    summary: str = Field(description="Booking options summary and recommendations")
