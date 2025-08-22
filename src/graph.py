"""Clean multi-agent supervisor graph with LangGraph interrupts."""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

from .agents import (
    create_booking_agent,
    create_search_agent,
    route_to_agent,
    supervisor_node,
)

load_dotenv()


class TravelPlannerGraph:
    """Multi-agent travel planner using supervisor pattern."""

    def __init__(self, enable_human_loop: bool = True, enable_memory: bool = True):
        self.search_agent = create_search_agent()
        self.booking_agent = create_booking_agent()
        self.enable_human_loop = enable_human_loop
        self.enable_memory = enable_memory
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the supervisor graph with interrupts."""
        workflow = StateGraph(MessagesState)

        # Add nodes
        workflow.add_node("supervisor", supervisor_node)
        workflow.add_node("search_agent", self.search_agent)
        workflow.add_node("booking_agent", self.booking_agent)

        # Define flow
        workflow.add_edge(START, "supervisor")
        workflow.add_conditional_edges(
            "supervisor",
            route_to_agent,
            {
                "search_agent": "search_agent",
                "booking_agent": "booking_agent",
                END: END,
            },
        )
        workflow.add_edge("search_agent", "supervisor")
        workflow.add_edge("booking_agent", "supervisor")

        # Compile with interrupts before booking agent
        interrupt_before = ["booking_agent"] if self.enable_human_loop else []

        if self.enable_memory:
            return workflow.compile(
                checkpointer=MemorySaver(), interrupt_before=interrupt_before
            )
        return workflow.compile(interrupt_before=interrupt_before)

    def chat(self, message: str, conversation_id: str = "demo") -> str | dict:
        """Chat interface with LangGraph interrupts."""
        config = (
            {"configurable": {"thread_id": conversation_id}}
            if self.enable_memory
            else {}
        )

        # Initial invoke
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]}, config=config
        )

        # Check if we were interrupted by examining the state (only if memory enabled)
        if self.enable_memory:
            state = self.graph.get_state(config)
            if state.next and "booking_agent" in state.next:
                # We were interrupted before booking agent - return interrupt info
                return {
                    "interrupted": True,
                    "message": "🔄 About to delegate to booking agent - requires human approval",
                    "user_request": message,
                    "conversation_id": conversation_id,
                    "next_step": state.next[0] if state.next else None,
                }

        # Extract final response if not interrupted
        for msg in reversed(result["messages"]):
            if hasattr(msg, "name") and msg.name in [
                "search_agent",
                "booking_agent",
                "supervisor",
            ]:
                return msg.content
            elif hasattr(msg, "content") and isinstance(msg, SystemMessage):
                return msg.content

        return "I'm ready to help you plan your travel!"

    def approve_and_continue(self, conversation_id: str = "demo") -> str:
        """Approve the interrupted workflow and let LangGraph continue automatically."""
        config = (
            {"configurable": {"thread_id": conversation_id}}
            if self.enable_memory
            else {}
        )

        # Simply invoke with None - LangGraph will resume from where it was interrupted
        result = self.graph.invoke(None, config=config)

        # Extract final response
        for msg in reversed(result["messages"]):
            if hasattr(msg, "name") and msg.name in [
                "search_agent",
                "booking_agent",
                "supervisor",
            ]:
                return msg.content
            elif hasattr(msg, "content") and isinstance(msg, SystemMessage):
                return msg.content

        return "Request processed."

    def reject_and_stop(self, conversation_id: str = "demo") -> str:
        """Reject the booking request and stop the workflow."""
        config = (
            {"configurable": {"thread_id": conversation_id}}
            if self.enable_memory
            else {}
        )

        # Add rejection message to state and end the workflow
        self.graph.update_state(
            config,
            {
                "messages": [
                    SystemMessage(
                        content="Booking request rejected by human supervisor."
                    )
                ]
            },
        )

        return "Booking request rejected by human supervisor."
