"""Multi-agent supervisor graph following LangGraph official patterns."""

from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from .agents import create_booking_agent, create_planning_agent, create_search_agent
from .config import get_llm_model

load_dotenv()


class TravelSupervisorGraph:
    """Professional multi-agent travel planner using supervisor pattern."""

    def __init__(self):
        """Initialize the supervisor graph with worker agents."""
        print("🔵 Initializing TravelSupervisorGraph...")

        # Create worker agents
        print("🔵 Creating worker agents...")
        self.search_agent = create_search_agent()
        self.planning_agent = create_planning_agent()
        self.booking_agent = create_booking_agent()

        # Supervisor is now just the supervisor_node function

        # Build the graph
        print("🔵 Building graph...")
        self.graph = self._build_graph()
        print("🔵 Graph built successfully")

    def supervisor_node(self, state: MessagesState):
        """Supervisor node that routes to agents or responds to user."""
        print("🔵 Supervisor analyzing...")

        # Check if we're getting a response from an agent
        last_message = state["messages"][-1]

        # If the last message is from an agent, supervisor should respond to user and end
        if hasattr(last_message, "name") and last_message.name in [
            "search_agent",
            "planning_agent",
            "booking_agent",
        ]:
            print(f"🔵 Received response from {last_message.name}, ending conversation")
            return {"next": "END"}

        # Otherwise, this is initial routing
        user_message = last_message.content
        print(f"🔵 User message: {user_message}")

        # Use LLM to make routing decision
        llm = get_llm_model()

        routing_prompt = f"""You are a travel planning supervisor. Analyze this user request and decide how to handle it.

User request: "{user_message}"

Available specialist agents:
- SEARCH: Find destinations, weather, location information
- PLANNING: Create itineraries, calculate budgets, plan trips  
- BOOKING: Search accommodations, flights, make reservations

Rules:
1. If it's travel-related, respond with exactly one word: SEARCH, PLANNING, or BOOKING
2. If it's completely off-topic (not about travel), respond with: REJECT

Your decision:"""

        response = llm.invoke(routing_prompt)
        decision = response.content.strip().upper()

        print(f"🔵 LLM routing decision: {decision}")

        if decision == "SEARCH":
            return {"next": "search_agent"}
        elif decision == "PLANNING":
            return {"next": "planning_agent"}
        elif decision == "BOOKING":
            return {"next": "booking_agent"}
        elif decision == "REJECT":
            # Add rejection message and end
            rejection_msg = SystemMessage(
                content="I'm a travel planning assistant. Please ask me about destinations, trip planning, or booking travel arrangements."
            )
            return {"messages": state["messages"] + [rejection_msg], "next": "END"}
        else:
            print(f"🔵 Unexpected decision: {decision}, defaulting to search")
            return {"next": "search_agent"}

    def _route_to_agent(
        self, state: MessagesState
    ) -> Literal["search_agent", "planning_agent", "booking_agent", END]:
        """Route to the appropriate agent based on supervisor's decision."""
        print(f"🔵 Routing based on supervisor decision")

        # The supervisor node should have set a "next" key
        if "next" in state:
            next_choice = state["next"]
            print(f"🔵 Supervisor chose: {next_choice}")

            if next_choice == "END":
                return END
            else:
                return next_choice

        # Fallback
        print("🔵 No routing decision found, defaulting to search_agent")
        return "search_agent"

    def _build_graph(self) -> StateGraph:
        """Build the supervisor graph following LangGraph patterns."""

        # Create the graph
        workflow = StateGraph(MessagesState)

        # Add all nodes
        workflow.add_node("supervisor", self.supervisor_node)
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
                END: END,
            },
        )

        # All agents return to supervisor
        workflow.add_edge("search_agent", "supervisor")
        workflow.add_edge("planning_agent", "supervisor")
        workflow.add_edge("booking_agent", "supervisor")

        return workflow.compile()

    def chat(self, message: str) -> str:
        """Simple chat interface."""
        print(f"🔵 Starting chat with: {message}")

        # Invoke the graph
        print("🔵 Invoking graph...")
        result = self.graph.invoke({"messages": [HumanMessage(content=message)]})
        print(f"🔵 Graph completed. Total messages: {len(result['messages'])}")

        # Extract the final response from the agent (not supervisor routing messages)
        agent_responses = []
        for i, msg in enumerate(result["messages"]):
            print(
                f"🔵 Message {i}: {type(msg).__name__} - {getattr(msg, 'name', 'no_name')}"
            )
            if hasattr(msg, "name") and msg.name in [
                "search_agent",
                "planning_agent",
                "booking_agent",
            ]:
                agent_responses.append(msg.content)
                print(f"🔵 Found agent response: {msg.content[:100]}...")

        # Return the last agent response, or a default if none found
        if agent_responses:
            print(f"🔵 Returning agent response")
            return agent_responses[-1]
        else:
            print(f"🔵 No agent responses found, returning default")
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
