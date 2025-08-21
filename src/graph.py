from datetime import datetime

from langgraph.graph import END, START, StateGraph

from .agents import BookAgent, PlanAgent, SearchAgent, SupervisorAgent
from .state import (
    AgentType,
    ExecutionResult,
    ExecutionStatus,
    ExecutionStep,
    WorkflowNode,
    WorkflowState,
)


class LangGraphTravelPlanner:
    def __init__(self):
        self.search_agent = SearchAgent()
        self.plan_agent = PlanAgent()
        self.book_agent = BookAgent()
        self.supervisor_agent = SupervisorAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(WorkflowState)

        workflow.add_node(WorkflowNode.SUPERVISOR, self._supervisor_node)

        workflow.add_edge(START, WorkflowNode.SUPERVISOR)

        workflow.add_node(WorkflowNode.SEARCH_EXECUTOR, self._search_executor_node)
        workflow.add_node(WorkflowNode.PLAN_EXECUTOR, self._plan_executor_node)
        workflow.add_node(WorkflowNode.BOOK_EXECUTOR, self._book_executor_node)

        workflow.add_conditional_edges(
            WorkflowNode.SUPERVISOR,
            self._route_to_executor,
            {
                AgentType.SEARCH: WorkflowNode.SEARCH_EXECUTOR,
                AgentType.PLAN: WorkflowNode.PLAN_EXECUTOR,
                AgentType.BOOK: WorkflowNode.BOOK_EXECUTOR,
            },
        )

        workflow.add_edge(WorkflowNode.SEARCH_EXECUTOR, END)
        workflow.add_edge(WorkflowNode.PLAN_EXECUTOR, END)
        workflow.add_edge(WorkflowNode.BOOK_EXECUTOR, END)

        return workflow.compile()

    def _supervisor_node(self, state: WorkflowState):
        step = ExecutionStep(
            step=WorkflowNode.SUPERVISOR,
            description="Analyzing request and routing to appropriate agent",
            input=state.input,
            timestamp=str(datetime.now()),
        )
        state.steps.append(step)

        try:
            result = self.supervisor_agent.process_request(state.input)

            if "output" in result and hasattr(result["output"], "agent_choice"):
                agent_choice = result["output"].agent_choice
                reasoning = result["output"].reasoning
            else:
                agent_choice = AgentType.SEARCH
                reasoning = "Default fallback to search agent"

        except Exception:
            agent_choice = AgentType.SEARCH
            reasoning = "Default fallback to search agent"

        step.output = f"Selected agent: {agent_choice.value}"
        step.reasoning = reasoning
        state.agent_choice = agent_choice
        return state

    def _route_to_executor(self, state: WorkflowState):
        return state.agent_choice

    def _search_executor_node(self, state: WorkflowState):
        step = ExecutionStep(
            step=WorkflowNode.SEARCH_EXECUTOR,
            description="Executing search operations",
            input=state.input,
            timestamp=str(datetime.now()),
        )
        state.steps.append(step)

        try:
            result = self.search_agent.process_request(state.input)
            step.output = result
            step.status = ExecutionStatus.SUCCESS
        except Exception as e:
            step.output = str(e)
            step.status = ExecutionStatus.ERROR

        state.result = result
        return state

    def _plan_executor_node(self, state: WorkflowState):
        step = ExecutionStep(
            step=WorkflowNode.PLAN_EXECUTOR,
            description="Creating travel plans and itineraries",
            input=state.input,
            timestamp=str(datetime.now()),
        )
        state.steps.append(step)

        try:
            result = self.plan_agent.process_request(state.input)
            step.output = result
            step.status = ExecutionStatus.SUCCESS
        except Exception as e:
            step.output = str(e)
            step.status = ExecutionStatus.ERROR

        state.result = result
        return state

    def _book_executor_node(self, state: WorkflowState):
        step = ExecutionStep(
            step=WorkflowNode.BOOK_EXECUTOR,
            description="Handling bookings and reservations",
            input=state.input,
            timestamp=str(datetime.now()),
        )
        state.steps.append(step)

        try:
            result = self.book_agent.process_request(state.input)
            step.output = result
            step.status = ExecutionStatus.SUCCESS
        except Exception as e:
            step.output = str(e)
            step.status = ExecutionStatus.ERROR

        state.result = result
        return state

    def process_request(self, user_input: str):
        initial_state = WorkflowState(input=user_input)
        result = self.graph.invoke(initial_state)

        return ExecutionResult(
            final_result=result.result,
            execution_steps=result.steps,
            agent_used=result.agent_choice,
        )
