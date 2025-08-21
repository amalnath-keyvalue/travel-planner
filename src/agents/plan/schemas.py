from typing import Dict, List

from pydantic import BaseModel, Field


class ItineraryResult(BaseModel):
    destination: str = Field(description="Destination name")
    days: int = Field(description="Number of days")
    daily_activities: List[str] = Field(description="Activities for each day")
    highlights: List[str] = Field(description="Key highlights and attractions")
    food_recommendations: List[str] = Field(
        description="Food and dining recommendations"
    )


class BudgetResult(BaseModel):
    destination: str = Field(description="Destination name")
    total_budget: float = Field(description="Total estimated budget")
    breakdown: Dict[str, float] = Field(description="Budget breakdown by category")
    daily_average: float = Field(description="Average daily cost")
    money_saving_tips: List[str] = Field(description="Tips to save money")
