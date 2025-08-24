"""Multi-agent travel planner graph."""

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
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
            add_handoff_back_messages=False,
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
        """Chat interface that returns responses from both supervisor and agents."""
        config = self.get_config(conversation_id)
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )

        messages = result["messages"]

        last_human_index = -1
        for i, msg in enumerate(messages):
            if isinstance(msg, HumanMessage):
                last_human_index = i

        ai_responses = []
        for i in range(last_human_index + 1, len(messages)):
            message = messages[i]
            if isinstance(message, AIMessage) and message.content:
                ai_responses.append(message.content)

        if not ai_responses:
            return "No response generated. Please try again."

        return "".join(ai_responses)
