"""Supervisor agent schemas."""

from pydantic import BaseModel, Field

from .constants import SupervisorAction


class SupervisorDecision(BaseModel):
    """Supervisor's autonomous decision on how to handle the request."""

    action: SupervisorAction = Field(
        description="Action to take: 'delegate_to_search', 'delegate_to_booking', 'handle_myself', or 'reject'"
    )
    reasoning: str = Field(description="Brief explanation for the decision")
    response: str = Field(
        description="Direct response to user if handling myself, otherwise empty",
        default="",
    )
