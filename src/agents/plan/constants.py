from langchain import hub

PLAN_AGENT_SYSTEM = """You are a travel planning specialist. Help users create itineraries and calculate budgets for their trips."""

ITINERARY_PROMPT = """Create a {days}-day travel itinerary for {destination} based on interests: {interests}. Include daily activities, recommendations, and estimated costs."""

BUDGET_PROMPT = """Calculate estimated budget for a {days}-day trip to {destination} with {accommodation_type} accommodation. Include breakdown of costs."""

REACT_PROMPT = hub.pull("hwchase17/react")
