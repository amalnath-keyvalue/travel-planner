"""Multi-agent travel planner graph."""

from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import GraphInterrupt
from langgraph.graph import END, START, MessagesState, StateGraph

from .agents import create_booking_agent, create_search_agent, create_supervisor_agent

load_dotenv()


def route_supervisor_output(state: MessagesState):
    """Route based on supervisor's tool usage."""
    messages = state.get("messages", [])
    if not messages:
        return END

    last_message = messages[-1]

    # If last message is from supervisor without tool calls, end conversation
    if getattr(last_message, "name", None) == "supervisor" and not (
        hasattr(last_message, "tool_calls") and last_message.tool_calls
    ):
        return END

    # Look for delegation tool calls from supervisor
    for message in reversed(messages):
        if (
            hasattr(message, "tool_calls")
            and message.tool_calls
            and getattr(message, "name", None) == "supervisor"
        ):
            for tool_call in message.tool_calls:
                if tool_call["name"] == "delegate_to_search_agent":
                    return "search_agent"
                elif tool_call["name"] == "delegate_to_booking_agent":
                    return "booking_agent"

    # Default to END
    return END


class TravelPlannerGraph:
    """Multi-agent travel planner using supervisor pattern."""

    def __init__(self, enable_human_loop: bool = True, enable_memory: bool = True):
        self.supervisor_agent = create_supervisor_agent()
        self.search_agent = create_search_agent()
        self.booking_agent = create_booking_agent()
        self.enable_human_loop = enable_human_loop
        self.enable_memory = enable_memory
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the supervisor graph."""
        workflow = StateGraph(MessagesState)

        # Add nodes
        workflow.add_node("supervisor", self.supervisor_agent)
        workflow.add_node("search_agent", self.search_agent)
        workflow.add_node("booking_agent", self.booking_agent)

        # Define flow
        workflow.add_edge(START, "supervisor")
        workflow.add_conditional_edges(
            "supervisor",
            route_supervisor_output,
            {
                "search_agent": "search_agent",
                "booking_agent": "booking_agent",
                END: END,
            },
        )
        workflow.add_edge("search_agent", "supervisor")
        workflow.add_edge("booking_agent", "supervisor")

        if self.enable_memory:
            return workflow.compile(checkpointer=MemorySaver())
        return workflow.compile()

    def get_config(self, conversation_id: str) -> dict[str, Any]:
        """Get configuration for the graph."""
        return (
            {"configurable": {"thread_id": conversation_id}, "recursion_limit": 10}
            if self.enable_memory
            else {"recursion_limit": 10}
        )

    def is_interrupted(self, state: MessagesState | None = None) -> bool:
        """Check if the workflow is interrupted."""
        return bool(state and state.next)

    def chat(self, message: str, conversation_id: str = "demo") -> str | dict:
        """Chat interface that handles both new messages and resumption."""
        config = self.get_config(conversation_id)

        try:
            # Get current state
            state = self.graph.get_state(config) if self.enable_memory else None

            if message.lower() in ["approve", "yes", "confirm"]:
                # Resume from interrupted state
                if not self.is_interrupted(state):
                    return "No pending booking to approve."

                # Resume the workflow
                result = self.graph.invoke(None, config=config)
                return result["messages"][-1].content

            # Start new conversation
            result = self.graph.invoke(
                {"messages": [HumanMessage(content=message)]},
                config=config,
            )

            # Check if we got interrupted
            state = self.graph.get_state(config) if self.enable_memory else None
            if self.is_interrupted(state):
                # Get the interrupt data from the state
                return {
                    "interrupted": True,
                    "data": state.next.get("data", {}),
                    "user_request": message,
                    "conversation_id": conversation_id,
                }

            # Return the last message
            return result["messages"][-1].content

        except GraphInterrupt as e:
            # Handle interrupts that come as exceptions
            interrupt_data = e.args[0][0].value if e.args and e.args[0] else {}
            if interrupt_data:
                return {
                    "interrupted": True,
                    "data": interrupt_data,
                    "user_request": message,
                    "conversation_id": conversation_id,
                }
            raise  # Re-raise if no data
        except Exception as e:
            raise  # Re-raise other exceptions
