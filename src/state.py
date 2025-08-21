from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    SEARCH = "search"
    PLAN = "plan"
    BOOK = "book"


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class WorkflowNode(str, Enum):
    SUPERVISOR = "supervisor"
    SEARCH_EXECUTOR = "search_executor"
    PLAN_EXECUTOR = "plan_executor"
    BOOK_EXECUTOR = "book_executor"


class SupervisorOutput(BaseModel):
    agent_choice: AgentType = Field(description="The selected agent type")
    reasoning: str = Field(description="Explanation for the agent choice")


class ExecutionStep(BaseModel):
    step: str
    description: str
    input: str
    timestamp: str
    output: Optional[str] = None
    reasoning: Optional[str] = None
    status: Optional[ExecutionStatus] = None


class ExecutionResult(BaseModel):
    final_result: str
    execution_steps: List[ExecutionStep]
    agent_used: AgentType


class WorkflowState(BaseModel):
    input: str
    steps: List[ExecutionStep] = []
    agent_choice: Optional[AgentType] = None
    result: Optional[str] = None


class ConversationMessage(BaseModel):
    role: MessageRole = Field(description="Role of the message sender")
    content: str = Field(description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str = Field(description="Agent that processed this message")


class AgentMemory(BaseModel):
    short_term: List[str] = Field(
        description="Recent context and decisions", default_factory=list
    )
    long_term: Dict[str, Any] = Field(
        description="Persistent user preferences and history", default_factory=dict
    )
    conversation_history: List[ConversationMessage] = Field(
        description="Full conversation history", default_factory=list
    )


class TravelRequest(BaseModel):
    destination: str = Field(description="Travel destination")
    budget: float = Field(description="Budget in USD")
    duration: int = Field(description="Trip duration in days")
    interests: List[str] = Field(description="Travel interests", default_factory=list)
    accommodation_type: str = Field(description="Preferred accommodation type")


class AgentState(BaseModel):
    messages: List[ConversationMessage] = Field(
        description="Current conversation messages"
    )
    current_agent: str = Field(description="Currently active agent")
    agent_response: str = Field(description="Response from the current agent")
    tools_used: List[str] = Field(description="Tools used in this interaction")
    memory: AgentMemory = Field(description="Agent memory and context")
    travel_request: TravelRequest = Field(
        description="Current travel request being processed"
    )
    workflow_step: str = Field(description="Current step in the workflow")
    confidence_score: float = Field(
        description="Confidence in the current response", ge=0.0, le=1.0
    )
