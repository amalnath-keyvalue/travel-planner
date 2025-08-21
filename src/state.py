from datetime import datetime

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: str = Field(description="Role of the message sender")
    content: str = Field(description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str = Field(description="Agent that processed this message")


class AgentMemory(BaseModel):
    short_term: list[str] = Field(
        description="Recent context and decisions", default_factory=list
    )
    long_term: dict = Field(
        description="Persistent user preferences and history", default_factory=dict
    )
    conversation_history: list[ConversationMessage] = Field(
        description="Full conversation history", default_factory=list
    )


class TravelRequest(BaseModel):
    destination: str = Field(description="Travel destination")
    budget: float = Field(description="Budget in USD")
    duration: int = Field(description="Trip duration in days")
    interests: list[str] = Field(description="Travel interests", default_factory=list)
    accommodation_type: str = Field(description="Preferred accommodation type")


class AgentState(BaseModel):
    messages: list[ConversationMessage] = Field(
        description="Current conversation messages"
    )
    current_agent: str = Field(description="Currently active agent")
    agent_response: str = Field(description="Response from the current agent")
    tools_used: list[str] = Field(description="Tools used in this interaction")
    memory: AgentMemory = Field(description="Agent memory and context")
    travel_request: TravelRequest = Field(
        description="Current travel request being processed"
    )
    workflow_step: str = Field(description="Current step in the workflow")
    confidence_score: float = Field(
        description="Confidence in the current response", ge=0.0, le=1.0
    )
