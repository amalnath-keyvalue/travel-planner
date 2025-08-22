"""Search agent schemas for external data."""

from pydantic import BaseModel, Field


class WeatherInfo(BaseModel):
    """Weather information from external API."""
    destination: str
    temperature_range: str = Field(description="Temperature range in Celsius")
    condition: str = Field(description="Current weather condition")
    rainfall_level: str = Field(description="Low/Medium/High rainfall")
    best_time_to_visit: str = Field(description="Optimal travel period")


class LocationInfo(BaseModel):
    """Basic location information from external API."""
    destination: str
    country: str
    timezone: str
    currency: str
    language: str
    visa_required: bool