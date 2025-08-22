"""Tools for the travel planning agents following LangChain patterns."""

import json

from langchain_core.tools import tool


@tool
def search_destinations(query: str, budget_level: str = "medium") -> str:
    """Search for travel destinations based on user preferences.

    Args:
        query: User's destination search query (e.g., "beach destinations", "cultural cities")
        budget_level: Budget preference (low, medium, high)

    Returns:
        JSON string with destination recommendations
    """
    # Simulate real destination search API
    destinations_db = {
        "beach": [
            {
                "name": "Bali, Indonesia",
                "country": "Indonesia",
                "avg_daily_cost": 60,
                "best_months": ["April", "May", "June", "September", "October"],
                "highlights": [
                    "Beautiful beaches",
                    "Hindu temples",
                    "Rice terraces",
                    "Vibrant culture",
                ],
                "climate": "Tropical",
            },
            {
                "name": "Santorini, Greece",
                "country": "Greece",
                "avg_daily_cost": 150,
                "best_months": ["May", "June", "September", "October"],
                "highlights": [
                    "Stunning sunsets",
                    "White architecture",
                    "Wine tasting",
                    "Volcanic beaches",
                ],
                "climate": "Mediterranean",
            },
            {
                "name": "Maldives",
                "country": "Maldives",
                "avg_daily_cost": 300,
                "best_months": ["November", "December", "January", "February", "March"],
                "highlights": [
                    "Luxury overwater bungalows",
                    "World-class diving",
                    "Pristine beaches",
                    "Complete privacy",
                ],
                "climate": "Tropical",
            },
        ],
        "cultural": [
            {
                "name": "Kyoto, Japan",
                "country": "Japan",
                "avg_daily_cost": 100,
                "best_months": ["March", "April", "May", "October", "November"],
                "highlights": [
                    "Ancient temples",
                    "Traditional gardens",
                    "Geisha districts",
                    "Cherry blossoms",
                ],
                "climate": "Temperate",
            },
            {
                "name": "Rome, Italy",
                "country": "Italy",
                "avg_daily_cost": 120,
                "best_months": ["April", "May", "September", "October"],
                "highlights": [
                    "Ancient ruins",
                    "Vatican City",
                    "Renaissance art",
                    "Italian cuisine",
                ],
                "climate": "Mediterranean",
            },
        ],
        "adventure": [
            {
                "name": "Queenstown, New Zealand",
                "country": "New Zealand",
                "avg_daily_cost": 140,
                "best_months": ["December", "January", "February", "March"],
                "highlights": [
                    "Bungee jumping",
                    "Skydiving",
                    "Hiking",
                    "Scenic beauty",
                ],
                "climate": "Temperate",
            }
        ],
    }

    # Smart matching based on query
    query_lower = query.lower()
    results = []

    if any(word in query_lower for word in ["beach", "island", "coast", "tropical"]):
        results.extend(destinations_db["beach"])
    if any(word in query_lower for word in ["culture", "history", "temple", "museum"]):
        results.extend(destinations_db["cultural"])
    if any(
        word in query_lower for word in ["adventure", "hiking", "extreme", "outdoor"]
    ):
        results.extend(destinations_db["adventure"])

    # If no specific category, return popular options
    if not results:
        results = destinations_db["beach"][:2] + destinations_db["cultural"][:2]

    # Filter by budget if specified
    budget_filters = {"low": 80, "medium": 150, "high": 500}
    max_budget = budget_filters.get(budget_level, 150)
    results = [d for d in results if d["avg_daily_cost"] <= max_budget]

    return json.dumps(
        {
            "destinations": results,
            "search_query": query,
            "budget_level": budget_level,
            "total_found": len(results),
        }
    )


@tool
def get_weather_forecast(destination: str, travel_month: str = "current") -> str:
    """Get weather forecast and best travel times for a destination.

    Args:
        destination: Destination name
        travel_month: Month of travel (optional)

    Returns:
        JSON string with weather information
    """
    # Simulate weather API
    weather_patterns = {
        "bali": {
            "temp_range": "26-30°C",
            "rainfall": "Medium",
            "best_months": ["Apr-Oct"],
        },
        "santorini": {
            "temp_range": "20-28°C",
            "rainfall": "Low",
            "best_months": ["May-Oct"],
        },
        "maldives": {
            "temp_range": "26-30°C",
            "rainfall": "Low",
            "best_months": ["Nov-Apr"],
        },
        "kyoto": {
            "temp_range": "15-25°C",
            "rainfall": "Medium",
            "best_months": ["Mar-May", "Oct-Nov"],
        },
        "rome": {
            "temp_range": "18-28°C",
            "rainfall": "Low",
            "best_months": ["Apr-Jun", "Sep-Oct"],
        },
        "queenstown": {
            "temp_range": "10-22°C",
            "rainfall": "Medium",
            "best_months": ["Dec-Mar"],
        },
    }

    dest_key = destination.lower().split(",")[0].strip()
    weather = weather_patterns.get(
        dest_key,
        {"temp_range": "20-25°C", "rainfall": "Medium", "best_months": ["Year-round"]},
    )

    return json.dumps(
        {
            "destination": destination,
            "travel_month": travel_month,
            "temperature_range": weather["temp_range"],
            "rainfall_level": weather["rainfall"],
            "best_travel_months": weather["best_months"],
            "weather_advice": f"Current conditions are generally favorable for travel to {destination}",
        }
    )


@tool
def create_detailed_itinerary(
    destination: str, duration_days: int, travel_style: str = "balanced"
) -> str:
    """Create a detailed day-by-day travel itinerary.

    Args:
        destination: Travel destination
        duration_days: Number of days for the trip
        travel_style: Style of travel (relaxed, balanced, packed)

    Returns:
        JSON string with detailed itinerary
    """
    # Base activities by destination type
    activity_templates = {
        "bali": [
            "Visit Tanah Lot Temple at sunset",
            "Explore Ubud Rice Terraces",
            "Traditional Balinese cooking class",
            "Beach day at Seminyak",
            "Visit Monkey Forest Sanctuary",
            "Sunrise hike at Mount Batur",
            "Traditional market shopping in Ubud",
        ],
        "santorini": [
            "Explore Oia village and sunset viewing",
            "Wine tasting tour in local vineyards",
            "Visit ancient Akrotiri archaeological site",
            "Beach day at Red Beach",
            "Fira to Oia hiking trail",
            "Traditional Greek cooking class",
            "Boat tour to nearby islands",
        ],
        "kyoto": [
            "Visit Fushimi Inari Shrine",
            "Explore Bamboo Grove in Arashiyama",
            "Traditional tea ceremony experience",
            "Visit Kinkaku-ji (Golden Pavilion)",
            "Walk through Gion geisha district",
            "Explore Philosopher's Path",
            "Visit Nijo Castle and gardens",
        ],
    }

    dest_key = destination.lower().split(",")[0].strip()
    activities = activity_templates.get(
        dest_key,
        [
            "City orientation walking tour",
            "Visit main cultural attractions",
            "Local cuisine food tour",
            "Shopping and leisure time",
            "Nature or outdoor activities",
            "Museum and gallery visits",
            "Local market exploration",
        ],
    )

    # Create daily itinerary
    daily_plans = []
    activities_per_day = (
        2 if travel_style == "relaxed" else 3 if travel_style == "balanced" else 4
    )

    for day in range(1, min(duration_days + 1, 8)):  # Cap at 7 days for demo
        day_activities = activities[
            (day - 1) * activities_per_day : day * activities_per_day
        ]
        if not day_activities:
            day_activities = activities[:activities_per_day]

        daily_plans.append(
            {
                "day": day,
                "morning": (
                    day_activities[0] if len(day_activities) > 0 else "Free time"
                ),
                "afternoon": (
                    day_activities[1]
                    if len(day_activities) > 1
                    else "Leisure exploration"
                ),
                "evening": (
                    day_activities[2]
                    if len(day_activities) > 2
                    else "Dinner and relaxation"
                ),
                "estimated_cost": f"${80 + (day * 10)}-{120 + (day * 15)}",
            }
        )

    return json.dumps(
        {
            "destination": destination,
            "duration": f"{duration_days} days",
            "travel_style": travel_style,
            "daily_itinerary": daily_plans,
            "total_estimated_cost": f"${duration_days * 100}-{duration_days * 150}",
            "notes": f"Itinerary optimized for {travel_style} travel pace",
        }
    )


@tool
def calculate_trip_budget(
    destination: str,
    duration_days: int,
    travel_style: str = "mid-range",
    travelers: int = 1,
) -> str:
    """Calculate comprehensive budget breakdown for a trip.

    Args:
        destination: Travel destination
        duration_days: Number of days
        travel_style: Budget style (budget, mid-range, luxury)
        travelers: Number of travelers

    Returns:
        JSON string with detailed budget breakdown
    """
    # Base daily costs by style
    cost_multipliers = {
        "budget": {"accommodation": 40, "food": 30, "activities": 25, "transport": 20},
        "mid-range": {
            "accommodation": 100,
            "food": 60,
            "activities": 50,
            "transport": 40,
        },
        "luxury": {
            "accommodation": 250,
            "food": 120,
            "activities": 100,
            "transport": 80,
        },
    }

    # Destination cost factors
    dest_factors = {
        "bali": 0.7,
        "santorini": 1.3,
        "maldives": 2.5,
        "kyoto": 1.2,
        "rome": 1.1,
        "queenstown": 1.4,
    }

    dest_key = destination.lower().split(",")[0].strip()
    dest_factor = dest_factors.get(dest_key, 1.0)

    base_costs = cost_multipliers.get(travel_style, cost_multipliers["mid-range"])

    # Apply destination factor and calculate totals
    daily_costs = {}
    for category, base_cost in base_costs.items():
        adjusted_cost = int(base_cost * dest_factor)
        if category == "accommodation":
            # Accommodation can be shared
            daily_costs[category] = adjusted_cost * (0.6 + 0.4 * travelers)
        else:
            # Other costs are per person
            daily_costs[category] = adjusted_cost * travelers

    total_daily = sum(daily_costs.values())
    total_trip = total_daily * duration_days

    return json.dumps(
        {
            "destination": destination,
            "duration": f"{duration_days} days",
            "travelers": travelers,
            "travel_style": travel_style,
            "daily_breakdown": {k: f"${int(v)}" for k, v in daily_costs.items()},
            "total_per_day": f"${int(total_daily)}",
            "total_trip_cost": f"${int(total_trip)}",
            "currency": "USD",
            "cost_factors": f"Destination factor: {dest_factor}x base costs",
        }
    )


@tool
def search_accommodations(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    budget_range: str = "mid-range",
) -> str:
    """Search for accommodation options at destination.

    Args:
        destination: Destination to search
        checkin_date: Check-in date (YYYY-MM-DD format)
        checkout_date: Check-out date (YYYY-MM-DD format)
        budget_range: Budget preference (budget, mid-range, luxury)

    Returns:
        JSON string with accommodation options
    """
    # Simulate accommodation search
    accommodation_templates = [
        {
            "name": "Grand Palace Hotel",
            "type": "Hotel",
            "rating": 4.5,
            "price_per_night": 150,
            "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym"],
            "location": "City Center",
        },
        {
            "name": "Boutique Heritage Inn",
            "type": "Boutique Hotel",
            "rating": 4.3,
            "price_per_night": 120,
            "amenities": ["WiFi", "Restaurant", "Historic Charm", "Rooftop Bar"],
            "location": "Historic District",
        },
        {
            "name": "Backpacker's Paradise Hostel",
            "type": "Hostel",
            "rating": 4.0,
            "price_per_night": 35,
            "amenities": ["WiFi", "Shared Kitchen", "Common Room", "Laundry"],
            "location": "Downtown",
        },
        {
            "name": "Luxury Resort & Spa",
            "type": "Resort",
            "rating": 4.8,
            "price_per_night": 300,
            "amenities": [
                "WiFi",
                "Multiple Pools",
                "Full Spa",
                "Private Beach",
                "Multiple Restaurants",
            ],
            "location": "Beachfront",
        },
    ]

    # Filter by budget
    budget_filters = {"budget": 60, "mid-range": 180, "luxury": 500}
    max_price = budget_filters.get(budget_range, 180)

    filtered_accommodations = [
        {
            **acc,
            "name": f"{acc['name']} - {destination}",
            "price_per_night": f"${acc['price_per_night']}",
        }
        for acc in accommodation_templates
        if acc["price_per_night"] <= max_price
    ]

    return json.dumps(
        {
            "destination": destination,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "budget_range": budget_range,
            "accommodations": filtered_accommodations,
            "total_options": len(filtered_accommodations),
        }
    )


@tool
def search_flights(
    origin: str, destination: str, departure_date: str, return_date: str = ""
) -> str:
    """Search for flight options between cities.

    Args:
        origin: Departure city
        destination: Destination city
        departure_date: Departure date (YYYY-MM-DD)
        return_date: Return date for round trip (optional)

    Returns:
        JSON string with flight options
    """
    # Simulate flight search
    airlines = ["Global Airways", "Sky Connect", "Premium Air", "Budget Wings"]
    aircraft_types = ["Boeing 737", "Airbus A320", "Boeing 777"]

    flight_options = []
    base_price = 400  # Base price for simulation

    for i, airline in enumerate(airlines):
        price_modifier = 1 + (i * 0.15)  # Different pricing tiers
        flight_options.append(
            {
                "airline": airline,
                "aircraft": aircraft_types[i % len(aircraft_types)],
                "departure_time": f"{6 + i*3}:30",
                "arrival_time": f"{14 + i*3}:45",
                "duration": f"{6 + i}h {15 + i*10}m",
                "price": f"${int(base_price * price_modifier)}",
                "stops": i % 2,  # Some direct, some with stops
                "baggage": "1 carry-on + 1 checked bag included",
            }
        )

    return json.dumps(
        {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "flight_options": flight_options,
            "total_options": len(flight_options),
            "search_timestamp": "2024-01-15T10:30:00Z",
        }
    )
