from langchain import hub

SEARCH_AGENT_SYSTEM = """You are a travel search specialist. Help users find destinations and check weather information. Use your tools to provide accurate and helpful responses."""

SEARCH_DESTINATIONS_PROMPT = """Find travel destinations for '{query}' within a budget of ${budget}. Provide 3-4 specific destinations with descriptions, estimated costs, and reasoning for the choices."""

WEATHER_PROMPT = """Provide current weather information for {destination}. Include temperature, conditions, and travel recommendations based on the weather."""

REACT_PROMPT = hub.pull("hwchase17/react")
