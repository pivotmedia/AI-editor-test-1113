"""
Story and article data models.
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class Story(BaseModel):
    """A story extracted from a homepage."""

    source: str = Field(..., description="Name of the news source")
    headline: str = Field(..., description="Story headline")
    summary: Optional[str] = Field(default=None, description="Short summary from homepage")
    url: HttpUrl = Field(..., description="URL to full article")
    category: Optional[str] = Field(default=None, description="Story category")
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="When the story was scraped")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "TechCrunch",
                "headline": "OpenAI launches new enterprise features",
                "summary": "The company announced several new tools for businesses...",
                "url": "https://techcrunch.com/2024/01/15/openai-enterprise",
                "category": "AI",
                "scraped_at": "2024-01-15T10:30:00Z"
            }
        }


class Article(BaseModel):
    """Full article content extracted from a story URL."""

    url: HttpUrl = Field(..., description="Article URL")
    source: str = Field(..., description="Source name")
    title: str = Field(..., description="Article title")
    content: str = Field(..., description="Full article text")
    author: Optional[str] = Field(default=None, description="Article author")
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")
    word_count: int = Field(..., description="Number of words in content")
    is_paywalled: bool = Field(default=False, description="Whether content is behind paywall")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="When extracted")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://techcrunch.com/2024/01/15/openai-enterprise",
                "source": "TechCrunch",
                "title": "OpenAI launches new enterprise features",
                "content": "Full article text here...",
                "author": "John Doe",
                "published_at": "2024-01-15T09:00:00Z",
                "word_count": 850,
                "is_paywalled": False,
                "extracted_at": "2024-01-15T10:30:00Z"
            }
        }


class ScoredArticle(BaseModel):
    """Article with relevance and impact scores."""

    article: Article = Field(..., description="The full article")
    relevance_score: int = Field(..., ge=0, le=100, description="AI relevance score (0-100)")
    impact_score: Optional[int] = Field(default=None, ge=0, le=100, description="Business impact score (0-100)")
    reasoning: Optional[str] = Field(default=None, description="Explanation of scores")

    class Config:
        json_schema_extra = {
            "example": {
                "article": {"url": "https://example.com", "title": "...", "content": "..."},
                "relevance_score": 85,
                "impact_score": 72,
                "reasoning": "High relevance due to corporate AI adoption angle..."
            }
        }


class StoryBullets(BaseModel):
    """Final summarized story with headline and bullets."""

    source: str = Field(..., description="Source name")
    url: HttpUrl = Field(..., description="Original article URL")
    headline: str = Field(..., description="Generated headline (10-14 words)")
    bullets: List[str] = Field(..., min_length=3, max_length=3, description="Exactly 3 bullet points")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "Reuters",
                "url": "https://reuters.com/article/12345",
                "headline": "Microsoft Expands Azure AI Services with New Enterprise Tools",
                "bullets": [
                    "Microsoft announced Azure AI Studio with custom model training for enterprises",
                    "The move positions Microsoft to compete directly with AWS and Google Cloud AI offerings",
                    "Early access customers report 40% reduction in AI deployment time"
                ]
            }
        }


class DailySummary(BaseModel):
    """Daily brief output with 5 top stories."""

    date: str = Field(..., description="Date in YYYY-MM-DD format")
    stories: List[StoryBullets] = Field(..., min_length=5, max_length=5, description="Exactly 5 stories")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When the summary was generated")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15",
                "stories": [
                    {
                        "source": "Reuters",
                        "url": "https://reuters.com/article/12345",
                        "headline": "Microsoft Expands Azure AI Services",
                        "bullets": ["...", "...", "..."]
                    }
                ],
                "generated_at": "2024-01-15T05:15:00Z"
            }
        }
