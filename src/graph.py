"""Multi-agent travel planner graph."""

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command
from langgraph_supervisor import create_supervisor

from .agents import create_booking_agent, create_search_agent
from .config import get_llm_model
from .constants import SUPERVISOR_PROMPT
from .tools import add_long_term_memory, search_long_term_memory
from .utils import debug_hook


class TravelPlannerGraph:
    """Multi-agent travel planner using supervisor pattern."""

    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the supervisor graph using langgraph-supervisor."""

        supervisor = create_supervisor(
            model=get_llm_model(),
            agents=[
                create_search_agent(),
                create_booking_agent(),
            ],
            tools=[add_long_term_memory, search_long_term_memory],
            prompt=SUPERVISOR_PROMPT,
            add_handoff_messages=False,
            add_handoff_back_messages=False,
            output_mode="full_history",
            pre_model_hook=lambda state: debug_hook(state, "SUPERVISOR_PRE"),
            post_model_hook=lambda state: debug_hook(state, "SUPERVISOR_POST"),
        )

        return supervisor.compile(
            checkpointer=MemorySaver(),
            store=InMemoryStore(),
        )

    def get_config(self, conversation_id: str) -> dict[str, Any]:
        """Get configuration for the graph."""
        return {"configurable": {"thread_id": conversation_id}}

    def chat(
        self,
        message: str,
        conversation_id: str = "demo",
        is_approved: bool | None = None,
    ) -> str | dict:
        """Chat interface that returns responses from both supervisor and agents."""
        config = self.get_config(conversation_id)

        if is_approved is not None:
            result = self.graph.invoke(
                Command(resume={"is_approved": is_approved}),
                config=config,
            )

        else:
            result = self.graph.invoke(
                {"messages": [HumanMessage(content=message)]},
                config=config,
            )

        if isinstance(result, dict) and "__interrupt__" in result:
            interrupt_data = result["__interrupt__"][0].value
            return {
                "type": "interrupt",
                "data": interrupt_data,
                "message": "Human approval required. Please respond to continue.",
            }

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

        if len(ai_responses) >= 2:
            return "".join(ai_responses[-2:])

        return "".join(ai_responses)
