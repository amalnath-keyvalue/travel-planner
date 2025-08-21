from typing import List

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    destinations: List[str] = Field(description="List of found destinations")
    descriptions: List[str] = Field(description="Descriptions for each destination")
    costs: List[float] = Field(description="Estimated costs for each destination")
    reasoning: str = Field(description="Why these destinations were chosen")


class WeatherResult(BaseModel):
    destination: str = Field(description="Destination name")
    temperature: str = Field(description="Current temperature")
    conditions: str = Field(description="Weather conditions")
    recommendations: List[str] = Field(
        description="Travel recommendations based on weather"
    )
