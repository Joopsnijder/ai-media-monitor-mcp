"""Article data model."""

from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    source: str
    date: datetime
    content: str | None = None
    summary: str | None = None
    mentions_ai: bool = False
    ai_topics: list[str] = []
    quoted_experts: list[dict[str, str]] = []
