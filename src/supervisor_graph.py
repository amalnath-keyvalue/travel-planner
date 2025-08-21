"""Multi-agent supervisor graph following LangGraph official patterns."""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent

from .agents import create_booking_agent, create_planning_agent, create_search_agent

load_dotenv()


class TravelSupervisorGraph:
    """Professional multi-agent travel planner using supervisor pattern."""

    def __init__(self):
        """Initialize the supervisor graph with worker agents."""
        # Create worker agents
        self.search_agent = create_search_agent()
        self.planning_agent = create_planning_agent()
        self.booking_agent = create_booking_agent()

        # Create supervisor agent
        self.supervisor_agent = self._create_supervisor_agent()

        # Build the graph
        self.graph = self._build_graph()

    def _create_supervisor_agent(self):
        """Create the supervisor agent with routing tools."""

        @tool
        def transfer_to_search_agent() -> str:
            """Call this when the user needs destination search or weather information."""
            return (
                "Transferring to search agent for destination and weather assistance."
            )

        @tool
        def transfer_to_planning_agent() -> str:
            """Call this when the user needs itinerary creation or budget planning."""
            return "Transferring to planning agent for itinerary and budget assistance."

        @tool
        def transfer_to_booking_agent() -> str:
            """Call this when the user needs accommodation or flight booking assistance."""
            return (
                "Transferring to booking agent for accommodation and flight assistance."
            )

        return create_react_agent(
            model=ChatGroq(
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name="llama3-70b-8192",
                temperature=0.1,
            ),
            tools=[
                transfer_to_search_agent,
                transfer_to_planning_agent,
                transfer_to_booking_agent,
            ],
            prompt=(
                "You are a travel planning supervisor managing three specialized agents:\n\n"
                "🔍 SEARCH AGENT: Handles destination search and weather information\n"
                "📋 PLANNING AGENT: Creates itineraries and calculates budgets\n"
                "🏨 BOOKING AGENT: Searches accommodations and flights\n\n"
                "ROUTING RULES:\n"
                "- For finding destinations, exploring places, weather queries → transfer_to_search_agent\n"
                "- For creating itineraries, planning trips, calculating budgets → transfer_to_planning_agent\n"
                "- For finding hotels, flights, booking assistance → transfer_to_booking_agent\n\n"
                "INSTRUCTIONS:\n"
                "- Analyze the user's request carefully\n"
                "- Route to the most appropriate agent based on the primary task\n"
                "- Use only ONE agent per request - do not call multiple agents\n"
                "- Provide a brief explanation of why you're routing to that agent\n"
                "- DO NOT attempt to answer travel questions yourself - always route to specialists"
            ),
            name="supervisor",
        )

    def _route_to_agent(
        self, state: MessagesState
    ) -> Literal["search_agent", "planning_agent", "booking_agent", "__end__"]:
        """Route to the appropriate agent based on supervisor's decision."""

        # Get the last message to see which tool the supervisor called
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            tool_name = last_message.tool_calls[0]["name"]

            if tool_name == "transfer_to_search_agent":
                return "search_agent"
            elif tool_name == "transfer_to_planning_agent":
                return "planning_agent"
            elif tool_name == "transfer_to_booking_agent":
                return "booking_agent"

        # Default routing based on message content if no tool was called
        content = str(state["messages"][-1].content).lower()

        if any(
            word in content
            for word in ["find", "search", "destination", "weather", "where", "explore"]
        ):
            return "search_agent"
        elif any(
            word in content
            for word in ["plan", "itinerary", "budget", "cost", "schedule", "days"]
        ):
            return "planning_agent"
        elif any(
            word in content
            for word in ["book", "hotel", "flight", "accommodation", "stay", "room"]
        ):
            return "booking_agent"
        else:
            return "search_agent"  # Default to search

    def _build_graph(self) -> StateGraph:
        """Build the supervisor graph following LangGraph patterns."""

        # Create the graph
        workflow = StateGraph(MessagesState)

        # Add all nodes
        workflow.add_node("supervisor", self.supervisor_agent)
        workflow.add_node("search_agent", self.search_agent)
        workflow.add_node("planning_agent", self.planning_agent)
        workflow.add_node("booking_agent", self.booking_agent)

        # Define the flow
        workflow.add_edge(START, "supervisor")

        # Conditional routing from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._route_to_agent,
            {
                "search_agent": "search_agent",
                "planning_agent": "planning_agent",
                "booking_agent": "booking_agent",
                "__end__": "__end__",
            },
        )

        # All agents return to supervisor for potential follow-up
        workflow.add_edge("search_agent", "supervisor")
        workflow.add_edge("planning_agent", "supervisor")
        workflow.add_edge("booking_agent", "supervisor")

        return workflow.compile()

    def chat(self, message: str) -> str:
        """Simple chat interface."""

        # Invoke the graph
        result = self.graph.invoke({"messages": [HumanMessage(content=message)]})

        # Extract the final response from the agent (not supervisor routing messages)
        agent_responses = []
        for msg in result["messages"]:
            if hasattr(msg, "name") and msg.name in [
                "search_agent",
                "planning_agent",
                "booking_agent",
            ]:
                agent_responses.append(msg.content)

        # Return the last agent response, or a default if none found
        if agent_responses:
            return agent_responses[-1]
        else:
            return "I'm ready to help you plan your travel! Ask me about destinations, planning, or booking."

    def stream_chat(self, message: str):
        """Stream the conversation for real-time responses."""

        for chunk in self.graph.stream({"messages": [HumanMessage(content=message)]}):
            if chunk:
                for node_name, node_update in chunk.items():
                    if "messages" in node_update:
                        for msg in node_update["messages"]:
                            if hasattr(msg, "name") and msg.name in [
                                "search_agent",
                                "planning_agent",
                                "booking_agent",
                            ]:
                                yield f"**{msg.name.replace('_', ' ').title()}**: {msg.content}"
                            elif hasattr(msg, "content") and not str(
                                msg.content
                            ).startswith("Transferring"):
                                yield msg.content

    def get_agent_info(self) -> dict:
        """Get information about available agents."""
        return {
            "supervisor": "Routes requests to specialized agents based on task type",
            "search_agent": "Finds destinations and provides weather information",
            "planning_agent": "Creates itineraries and calculates budgets",
            "booking_agent": "Searches accommodations and flights",
        }
