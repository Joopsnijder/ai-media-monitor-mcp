"""Unit tests for data models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.ai_media_monitor.models import (
    Article,
    Config,
    Expert,
    MediaSource,
    PaywallService,
    TopicSuggestion,
    TrendingTopic,
)


class TestMediaSource:
    """Tests for MediaSource model."""

    def test_valid_media_source(self):
        """Test creation of valid MediaSource."""
        source = MediaSource(
            name="NRC",
            url="https://www.nrc.nl",
            rss="https://www.nrc.nl/rss/",
            categories=["tech", "politics"],
        )
        assert source.name == "NRC"
        assert source.url == "https://www.nrc.nl"
        assert source.rss == "https://www.nrc.nl/rss/"
        assert source.categories == ["tech", "politics"]

    def test_media_source_without_rss(self):
        """Test MediaSource without RSS feed."""
        source = MediaSource(name="Test", url="https://test.com")
        assert source.rss is None
        assert source.categories == []

    def test_media_source_validation(self):
        """Test MediaSource validation."""
        with pytest.raises(ValidationError):
            MediaSource()  # Missing required fields


class TestPaywallService:
    """Tests for PaywallService model."""

    def test_valid_paywall_service(self):
        """Test creation of valid PaywallService."""
        service = PaywallService(url="https://archive.ph", method="POST", priority=1)
        assert service.url == "https://archive.ph"
        assert service.method == "POST"
        assert service.priority == 1

    def test_paywall_service_defaults(self):
        """Test PaywallService with defaults."""
        service = PaywallService(url="https://12ft.io")
        assert service.method == "GET"
        assert service.priority == 1


class TestConfig:
    """Tests for Config model."""

    def test_valid_config(self):
        """Test creation of valid Config."""
        config = Config(
            media_sources={
                "newspapers": [
                    MediaSource(name="NRC", url="https://nrc.nl", rss="https://nrc.nl/rss")
                ]
            },
            paywall_services=[PaywallService(url="https://archive.ph", method="POST")],
            retry_attempts=3,
            timeout=30,
            rate_limit=10,
        )
        assert len(config.media_sources["newspapers"]) == 1
        assert len(config.paywall_services) == 1
        assert config.retry_attempts == 3

    def test_config_defaults(self):
        """Test Config with defaults."""
        config = Config(media_sources={}, paywall_services=[])
        assert config.retry_attempts == 3
        assert config.timeout == 30
        assert config.rate_limit == 10


class TestArticle:
    """Tests for Article model."""

    def test_valid_article(self):
        """Test creation of valid Article."""
        article = Article(
            title="AI in Healthcare",
            url="https://example.com/article",
            source="NRC",
            date=datetime.now(),
            content="AI is transforming healthcare...",
            summary="Article about AI in healthcare",
            mentions_ai=True,
            ai_topics=["AI in de zorg"],
            quoted_experts=[{"name": "Dr. Smith", "quote": "AI helps doctors"}],
        )
        assert article.title == "AI in Healthcare"
        assert article.mentions_ai is True
        assert "AI in de zorg" in article.ai_topics
        assert len(article.quoted_experts) == 1

    def test_article_defaults(self):
        """Test Article with defaults."""
        article = Article(
            title="Test Article", url="https://test.com", source="Test Source", date=datetime.now()
        )
        assert article.content is None
        assert article.summary is None
        assert article.mentions_ai is False
        assert article.ai_topics == []
        assert article.quoted_experts == []


class TestExpert:
    """Tests for Expert model."""

    def test_valid_expert(self):
        """Test creation of valid Expert."""
        expert = Expert(
            name="Dr. Jan de Vries",
            title="Professor",
            organization="TU Delft",
            expertise=["AI", "Machine Learning"],
            recent_quotes=5,
            articles=[],
            contact_hints=["LinkedIn", "University website"],
        )
        assert expert.name == "Dr. Jan de Vries"
        assert expert.title == "Professor"
        assert expert.organization == "TU Delft"
        assert len(expert.expertise) == 2
        assert expert.recent_quotes == 5

    def test_expert_defaults(self):
        """Test Expert with defaults."""
        expert = Expert(name="Test Expert")
        assert expert.title is None
        assert expert.organization is None
        assert expert.expertise == []
        assert expert.recent_quotes == 0
        assert expert.articles == []
        assert expert.contact_hints == []


class TestTrendingTopic:
    """Tests for TrendingTopic model."""

    def test_valid_trending_topic(self):
        """Test creation of valid TrendingTopic."""
        topic = TrendingTopic(
            topic="AI in de zorg",
            mentions=10,
            sources=["NRC", "Volkskrant"],
            sentiment="positive",
            key_articles=[],
            suggested_angle="Healthcare AI success stories",
            growth_percentage=25.5,
        )
        assert topic.topic == "AI in de zorg"
        assert topic.mentions == 10
        assert len(topic.sources) == 2
        assert topic.sentiment == "positive"
        assert topic.growth_percentage == 25.5

    def test_trending_topic_defaults(self):
        """Test TrendingTopic with defaults."""
        topic = TrendingTopic(topic="Test Topic", mentions=5, sources=["Source1"])
        assert topic.sentiment == "neutral"
        assert topic.key_articles == []
        assert topic.suggested_angle is None
        assert topic.growth_percentage is None


class TestTopicSuggestion:
    """Tests for TopicSuggestion model."""

    def test_valid_topic_suggestion(self):
        """Test creation of valid TopicSuggestion."""
        suggestion = TopicSuggestion(
            topic="AI Privacy",
            relevance_score=8.5,
            reason="High mentions and expert availability",
            potential_guests=[],
            unique_angle="Privacy challenges in Dutch AI implementation",
            questions=["How do you handle privacy?", "What are the challenges?"],
        )
        assert suggestion.topic == "AI Privacy"
        assert suggestion.relevance_score == 8.5
        assert suggestion.reason == "High mentions and expert availability"
        assert len(suggestion.questions) == 2

    def test_topic_suggestion_defaults(self):
        """Test TopicSuggestion with defaults."""
        suggestion = TopicSuggestion(
            topic="Test Topic", relevance_score=5.0, reason="Test reason", unique_angle="Test angle"
        )
        assert suggestion.potential_guests == []
        assert suggestion.questions == []
