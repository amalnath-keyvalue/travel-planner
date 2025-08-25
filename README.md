# Multi-Agent Travel Planner

A travel planning system using LangGraph and Groq with 3 specialized agents.

## Features

- **Supervisor Agent**: Routes requests and presents results
- **Search Agent**: Weather, location information, and travel planning
- **Booking Agent**: Hotel and flight bookings with approval flow

## Setup

```bash
# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

## Usage

### 🌐 Streamlit Web App

```bash
# Run the Streamlit app
poetry run streamlit run streamlit_app.py
```

Opens at `http://localhost:8501` with chat interface and agent responses.

## Architecture

- **Supervisor Pattern**: Central router with specialist agents
- **Pydantic Models**: Structured data validation
- **LangGraph**: Checkpointing, interrupts, state management
- **Memory System**: Session-based memory with embeddings
- **Tool Integration**: Mock APIs for weather, flights, and hotels

## Tools & Capabilities

**Search Agent Tools:**
- Weather forecasts with temperature and rainfall data
- Location information (timezone, currency, visa requirements)

**Booking Agent Tools:**
- Hotel search with amenities and pricing
- Flight search with airline options and pricing
- Booking confirmation workflows
