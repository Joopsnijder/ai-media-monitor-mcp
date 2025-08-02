"""Expert data model."""

from pydantic import BaseModel

from .article import Article


class Expert(BaseModel):
    name: str
    title: str | None = None
    organization: str | None = None
    expertise: list[str] = []
    recent_quotes: int = 0
    articles: list[Article] = []
    contact_hints: list[str] = []
