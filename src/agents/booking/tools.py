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
    destination: str,
    check_in: str,
    guests: int,
    check_out: str | None = None,
) -> AccommodationSearch:
    """Search for available accommodations in a destination."""
    if not destination or destination.strip() == "":
        raise ValueError("Destination cannot be empty")
    if not check_in or check_in.strip() == "":
        raise ValueError("Check-in date cannot be empty")
    if not guests:
        raise ValueError("Guests number cannot be empty")

    print(
        f"search_accommodations: destination={destination}, check_in={check_in}, check_out={check_out}, guests={guests}"
    )
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
        guests=guests,
        options=accommodations,
    )


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str | None = None,
) -> FlightSearch:
    """Search for available flights between destinations."""
    if not origin or origin.strip() == "":
        raise ValueError("Origin cannot be empty")
    if not destination or destination.strip() == "":
        raise ValueError("Destination cannot be empty")
    if not departure_date or departure_date.strip() == "":
        raise ValueError("Departure date cannot be empty")

    is_roundtrip = return_date is not None
    print(
        f"search_flights: origin={origin}, destination={destination}, departure_date={departure_date}, "
        f"return_date={return_date}"
    )
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


@tool
def confirm_accommodation_booking(
    accommodation_name: str,
    destination: str,
    check_in: str,
    check_out: str,
    guest_name: str,
    payment_method: str,
) -> BookingResponse:
    """Complete a hotel booking. Requires human approval for security."""
    print(
        f"confirm_accommodation_booking: accommodation_name={accommodation_name}, destination={destination}, check_in={check_in}, "
        f"check_out={check_out}, guest_name={guest_name}, payment_method={payment_method}"
    )
    booking_ref = f"HTL{random.randint(100000, 999999)}"
    return BookingResponse(
        status="confirmed",
        booking_reference=booking_ref,
        details=f"Booking confirmed for {accommodation_name} in {destination}",
        confirmation_message=f"Your accommodation booking is confirmed! Reference: {booking_ref}",
    )


@tool
def confirm_flight_booking(
    airline: str,
    route: str,
    departure_date: str,
    passenger_name: str,
    payment_method: str,
) -> BookingResponse:
    """Complete a flight booking. Requires human approval for security."""
    print(
        f"confirm_flight_booking: airline={airline}, route={route}, departure_date={departure_date}, "
        f"passenger_name={passenger_name}, payment_method={payment_method}"
    )
    booking_ref = f"FLT{random.randint(100000, 999999)}"
    return BookingResponse(
        status="confirmed",
        booking_reference=booking_ref,
        details=f"Flight booking confirmed with {airline} for {route}",
        confirmation_message=f"Your flight booking is confirmed! Reference: {booking_ref}",
    )
