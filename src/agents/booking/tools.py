"""Booking agent tools for accommodations and flights."""

import random

from langchain_core.tools import tool

from .schemas import (
    Accommodation,
    AccommodationSearch,
    BookingResponse,
    Flight,
    FlightSearch,
)


@tool
def search_accommodations(
    destination: str, check_in: str, check_out: str, guests: str = "2"
) -> AccommodationSearch:
    """Search for accommodation options in a destination."""

    try:
        num_guests = int(guests)
    except:
        num_guests = 2

    # Simple demo accommodations
    accommodations = [
        Accommodation(
            name="Beach Resort",
            type="Resort",
            price_per_night=300,
            rating=4.5,
            amenities=["Pool", "WiFi"],
            pros="Great location",
            cons="Expensive",
        ),
        Accommodation(
            name="Budget Hotel",
            type="Hotel",
            price_per_night=80,
            rating=4.0,
            amenities=["WiFi", "Breakfast"],
            pros="Affordable",
            cons="Basic facilities",
        ),
    ]

    return AccommodationSearch(
        destination=destination,
        check_in=check_in,
        check_out=check_out,
        guests=num_guests,
        options=accommodations,
        booking_tips=["Book early for better rates"],
    )


@tool
def search_flights(
    origin: str, destination: str, departure_date: str, return_date: str = None
) -> FlightSearch:
    """Search for flight options between origin and destination."""

    # Simple demo flights
    is_roundtrip = return_date is not None

    flights = [
        Flight(
            airline="Demo Airways",
            price=500 if not is_roundtrip else 900,
            rating=4.2,
            departure_time="10:00",
            duration="8h 30m",
            stops=0,
            travel_class="Economy",
        ),
        Flight(
            airline="Budget Air",
            price=300 if not is_roundtrip else 550,
            rating=3.8,
            departure_time="14:30",
            duration="9h 15m",
            stops=1,
            travel_class="Economy",
        ),
    ]

    return FlightSearch(
        route=f"{origin} → {destination}",
        departure_date=departure_date,
        return_date=return_date,
        is_roundtrip=is_roundtrip,
        options=flights,
        booking_tips=["Book early for better prices"],
    )
