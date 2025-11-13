"""
Source configuration models.
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class SourceConfig(BaseModel):
    """Configuration for a news source."""

    name: str = Field(..., description="Name of the news source")
    homepage_url: HttpUrl = Field(..., description="Homepage URL to scrape")
    category: str = Field(..., description="Category (business, tech, general)")
    enabled: bool = Field(default=True, description="Whether this source is active")
    priority: int = Field(default=2, description="Priority level (1=highest, 3=lowest)")
    notes: Optional[str] = Field(default=None, description="Additional notes about the source")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TechCrunch",
                "homepage_url": "https://techcrunch.com",
                "category": "tech",
                "enabled": True,
                "priority": 1,
                "notes": "Strong AI coverage"
            }
        }
