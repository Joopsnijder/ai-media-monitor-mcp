"""Configuration models."""


from pydantic import BaseModel


class MediaSource(BaseModel):
    name: str
    url: str
    rss: str | None = None
    categories: list[str] = []


class PaywallService(BaseModel):
    url: str
    method: str = "GET"
    priority: int = 1


class Config(BaseModel):
    media_sources: dict[str, list[MediaSource]]
    paywall_services: list[PaywallService]
    retry_attempts: int = 3
    timeout: int = 30
    rate_limit: int = 10
