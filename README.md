# Travel Planner Agent

A simple travel planning system with 3 agents using LangGraph and ChatGroq, featuring both a command-line interface and a modern Streamlit web app.

## Setup

```bash
# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### 🌐 Streamlit Web App (Recommended)

```bash
# Run the Streamlit app
poetry run streamlit run streamlit_app.py

# Or use the helper script
python run_streamlit.py
```

The Streamlit app will open in your browser at `http://localhost:8501` and provides:
- Interactive chat interface with travel agents
- Quick action buttons for common queries
- Real-time responses from your AI agents
- Chat history and conversation management
- Beautiful, modern UI

### 💻 Command Line Interface

```bash
# Run the demo
poetry run python main.py

# Or use the Poetry script
poetry run travel-planner
```

## Architecture

- **Search Agent**: Finds destinations and checks weather
- **Plan Agent**: Creates itineraries and calculates budgets  
- **Book Agent**: Finds accommodation and confirms bookings
- **LangGraph**: Orchestrates workflow between agents
- **ChatGroq**: Provides LLM capabilities for each agent

## Environment Variables

```bash
GROQ_API_KEY=your_groq_api_key
```

## Features

### ✨ Streamlit App Features
- **Interactive Chat**: Natural language queries to travel agents
- **Quick Actions**: Pre-built buttons for common travel questions
- **Real-time Processing**: Live responses from your AI agents
- **Chat History**: Persistent conversation tracking
- **Responsive Design**: Works on desktop and mobile devices
- **API Key Management**: Secure input for your Groq API key

### 🔧 Technical Features
- **Multi-Agent System**: Coordinated workflow between specialized agents
- **LangGraph Integration**: Robust conversation flow management
- **Error Handling**: Graceful error handling and user feedback
- **Session Management**: Persistent state across app interactions
