"""Topic-related data models."""

from pydantic import BaseModel

from .article import Article
from .expert import Expert


class TrendingTopic(BaseModel):
    topic: str
    mentions: int
    sources: list[str]
    sentiment: str = "neutral"
    key_articles: list[Article] = []
    suggested_angle: str | None = None
    growth_percentage: float | None = None


class TopicSuggestion(BaseModel):
    topic: str
    relevance_score: float
    reason: str
    potential_guests: list[Expert] = []
    unique_angle: str
    questions: list[str] = []
