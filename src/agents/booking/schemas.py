"""Booking agent schemas."""

from typing import List, Optional

from pydantic import BaseModel


class Accommodation(BaseModel):
    """Accommodation details."""

    name: str
    type: str
    price_per_night: float
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


class Flight(BaseModel):
    """Flight details."""

    airline: str
    price: float
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
    """Booking confirmation response."""

    status: str
    booking_reference: str
    details: str
    confirmation_message: str
