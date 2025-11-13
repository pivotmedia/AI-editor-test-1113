"""
Configuration management for AI Editor using Pydantic Settings.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # API Keys
    firecrawl_api_key: str = Field(..., description="Firecrawl API key")
    anthropic_api_key: str = Field(..., description="Anthropic Claude API key")

    # Application Settings
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="development", description="Environment name")

    # Filtering Thresholds
    ai_relevance_threshold: int = Field(default=40, description="Minimum AI relevance score (0-100)")
    min_article_word_count: int = Field(default=200, description="Minimum article word count")

    # Scheduling
    daily_run_time: str = Field(default="05:00", description="Daily run time (HH:MM)")
    timezone: str = Field(default="America/New_York", description="Timezone for scheduling")

    # Output Settings
    output_dir: str = Field(default="output", description="Output directory for JSON files")

    # Firecrawl Settings
    firecrawl_timeout: int = Field(default=30, description="Firecrawl request timeout in seconds")
    firecrawl_max_retries: int = Field(default=3, description="Max retries for Firecrawl requests")

    # LLM Settings
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", description="Claude model to use")
    anthropic_max_tokens: int = Field(default=2000, description="Max tokens for Claude responses")
    anthropic_temperature: float = Field(default=0.3, description="Temperature for Claude responses")


# Global settings instance
settings = Settings()
