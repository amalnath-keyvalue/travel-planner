# Multi-Agent Travel Planner

A simple travel planning system using LangGraph and Groq.

## Features

### 🤖 Multi-Agent Architecture
- **Supervisor Agent**: Routes requests and handles general planning
- **Search Agent**: Handles weather and location information
- **Booking Agent**: Manages hotel and flight bookings with approval flow

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

The app will open at `http://localhost:8501` with:
- Interactive chat interface
- Example suggestions
- Real-time agent responses
- Natural booking approvals

## Technical Details

### 🏗️ Architecture
- **Supervisor Pattern**: Central router with specialist agents
- **Tool-Based Delegation**: LLM-driven routing decisions
- **Pydantic Models**: Structured data validation
- **LangGraph Features**: Checkpointing, interrupts, state management

### 🔧 Agent Capabilities
- **Supervisor**: General planning, request routing, direct responses
- **Search**: Weather info, location details, travel data
- **Booking**: Hotel search, flight search, booking confirmations
