from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from src.agents import BookAgent, PlanAgent, SearchAgent
from src.config import Config


class LangGraphTravelPlanner:
    def __init__(self):
        self.search_agent = SearchAgent()
        self.plan_agent = PlanAgent()
        self.book_agent = BookAgent()
        self.llm = Config.get_llm()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(dict)

        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("search_executor", self._search_executor_node)
        workflow.add_node("plan_executor", self._plan_executor_node)
        workflow.add_node("book_executor", self._book_executor_node)

        workflow.set_entry_point("supervisor")

        workflow.add_conditional_edges(
            "supervisor",
            self._route_to_executor,
            {
                "search": "search_executor",
                "plan": "plan_executor",
                "book": "book_executor",
            },
        )

        workflow.add_edge("search_executor", END)
        workflow.add_edge("plan_executor", END)
        workflow.add_edge("book_executor", END)

        return workflow.compile()

    def _supervisor_node(self, state):
        user_input = state["input"]

        messages = [
            SystemMessage(
                content="You are a travel planning supervisor. Choose the appropriate agent: search (destinations/weather), plan (itineraries/budgets), or book (accommodation/bookings)."
            ),
            HumanMessage(
                content=f"Request: {user_input}\n\nChoose: search, plan, or book"
            ),
        ]

        response = self.llm.invoke(messages)
        content = response.content.lower()

        if "search" in content:
            agent_choice = "search"
        elif "plan" in content:
            agent_choice = "plan"
        elif "book" in content:
            agent_choice = "book"
        else:
            agent_choice = "search"

        state["agent_choice"] = agent_choice
        return state

    def _route_to_executor(self, state):
        return state["agent_choice"]

    def _search_executor_node(self, state):
        result = self.search_agent.process_request(state["input"])
        state["result"] = result
        return state

    def _plan_executor_node(self, state):
        result = self.plan_agent.process_request(state["input"])
        state["result"] = result
        return state

    def _book_executor_node(self, state):
        result = self.book_agent.process_request(state["input"])
        state["result"] = result
        return state

    def process_request(self, user_input: str):
        initial_state = {"input": user_input}
        result = self.graph.invoke(initial_state)
        return result["result"]
