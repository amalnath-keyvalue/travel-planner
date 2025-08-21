from langchain import hub

BOOK_AGENT_SYSTEM = """You are a travel booking specialist. Help users find accommodation and confirm bookings."""

ACCOMMODATION_PROMPT = """Find accommodation options in {destination} within budget ${budget} for {accommodation_type} type. Provide 3-4 options with prices and features."""

BOOKING_PROMPT = """Confirm booking for {accommodation} in {destination} for dates {dates} at price ${price}. Provide booking confirmation details."""

REACT_PROMPT = hub.pull("hwchase17/react")
