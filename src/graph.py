"""Multi-agent travel planner graph."""

from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph_supervisor import create_supervisor

from .agents import create_booking_agent, create_search_agent
from .config import get_llm_model
from .constants import SUPERVISOR_PROMPT


class TravelPlannerGraph:
    """Multi-agent travel planner using supervisor pattern."""

    def __init__(
        self,
        enable_memory: bool = True,
    ):
        self.enable_memory = enable_memory
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the supervisor graph using langgraph-supervisor."""

        def _debug_hook(event: str):
            print("\n🔍 SUPERVISOR DEBUG:")
            print(f"   Event: {event}")

        supervisor = create_supervisor(
            model=get_llm_model(),
            agents=[
                create_search_agent(),
                create_booking_agent(),
            ],
            prompt=SUPERVISOR_PROMPT,
            add_handoff_back_messages=True,
            output_mode="full_history",
            post_model_hook=_debug_hook,
        )

        if self.enable_memory:
            return supervisor.compile(checkpointer=MemorySaver())
        return supervisor.compile()

    def get_config(self, conversation_id: str) -> dict[str, Any]:
        """Get configuration for the graph."""
        return {"configurable": {"thread_id": conversation_id}}

    def chat(self, message: str, conversation_id: str = "demo") -> str | dict:
        """Chat interface that handles both new messages and resumption."""
        config = self.get_config(conversation_id)
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
        return result["messages"][-1].content
