"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.fixtures.sample_data import (
    SAMPLE_ARTICLES,
    SAMPLE_CONFIG,
    SAMPLE_EXPERTS,
    SAMPLE_RSS_FEEDS,
    SAMPLE_TOPIC_SUGGESTIONS,
    SAMPLE_TRENDING_TOPICS,
    get_sample_articles_by_timeframe,
    get_sample_experts_by_topic,
    get_sample_trending_topics_by_period,
)


@pytest.fixture
def sample_article():
    """Provide a sample article for testing."""
    return SAMPLE_ARTICLES["ai_healthcare"]


@pytest.fixture
def sample_articles():
    """Provide sample articles for testing."""
    return list(SAMPLE_ARTICLES.values())


@pytest.fixture
def sample_expert():
    """Provide a sample expert for testing."""
    return SAMPLE_EXPERTS[0]


@pytest.fixture
def sample_experts():
    """Provide sample experts for testing."""
    return SAMPLE_EXPERTS


@pytest.fixture
def sample_trending_topic():
    """Provide a sample trending topic for testing."""
    return SAMPLE_TRENDING_TOPICS[0]


@pytest.fixture
def sample_trending_topics():
    """Provide sample trending topics for testing."""
    return SAMPLE_TRENDING_TOPICS


@pytest.fixture
def sample_topic_suggestion():
    """Provide a sample topic suggestion for testing."""
    return SAMPLE_TOPIC_SUGGESTIONS[0]


@pytest.fixture
def sample_topic_suggestions():
    """Provide sample topic suggestions for testing."""
    return SAMPLE_TOPIC_SUGGESTIONS


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return SAMPLE_CONFIG


@pytest.fixture
def sample_rss_feeds():
    """Provide sample RSS feeds for testing."""
    return SAMPLE_RSS_FEEDS


@pytest.fixture
def mock_analyzer():
    """Provide a mock MediaAnalyzer for testing."""
    analyzer = MagicMock()

    # Mock scan_media_sources method
    analyzer.scan_media_sources = AsyncMock(
        return_value={
            "scan_date": "2024-01-01T12:00:00",
            "hours_scanned": 24,
            "total_articles": len(SAMPLE_ARTICLES),
            "articles": list(SAMPLE_ARTICLES.values()),
            "trending_topics": SAMPLE_TRENDING_TOPICS,
            "potential_guests": SAMPLE_EXPERTS[:3],
        }
    )

    # Mock fetch_article method
    analyzer.fetch_article = AsyncMock(
        return_value={
            "url": "https://example.com/article",
            "title": "Test Article",
            "content_preview": "This is a test article...",
            "is_ai_related": True,
            "ai_topics": ["AI", "Technology"],
            "quoted_experts": [],
            "fetch_successful": True,
        }
    )

    # Mock parse_article method
    analyzer.parse_article = MagicMock(return_value=SAMPLE_ARTICLES["ai_healthcare"])

    return analyzer


@pytest.fixture
def mock_mcp_context():
    """Provide a mock MCP context for testing."""
    context = MagicMock()
    context.session_id = "test-session-123"
    return context


@pytest.fixture
def articles_by_timeframe():
    """Provide articles filtered by timeframe."""
    return get_sample_articles_by_timeframe


@pytest.fixture
def experts_by_topic():
    """Provide experts filtered by topic."""
    return get_sample_experts_by_topic


@pytest.fixture
def trending_topics_by_period():
    """Provide trending topics filtered by period."""
    return get_sample_trending_topics_by_period


@pytest.fixture
def dutch_ai_terms():
    """Provide Dutch AI-related terms for testing."""
    return [
        "kunstmatige intelligentie",
        "machine learning",
        "deep learning",
        "AI",
        "algoritme",
        "chatbot",
        "automatisering",
        "robotica",
        "data science",
        "neuraal netwerk",
    ]


@pytest.fixture
def mock_web_scraper():
    """Provide a mock web scraper for testing."""
    scraper = MagicMock()
    scraper.fetch_content = AsyncMock(
        return_value={
            "success": True,
            "content": "Sample article content with AI keywords...",
            "title": "Test Article",
            "byline": "By Test Author",
        }
    )
    return scraper


@pytest.fixture
def mock_rss_parser():
    """Provide a mock RSS parser for testing."""
    parser = MagicMock()
    parser.parse_feed = MagicMock(
        return_value=[
            {
                "title": "AI News Article",
                "link": "https://example.com/article1",
                "description": "An article about AI developments",
                "published": "2024-01-01T10:00:00Z",
            },
            {
                "title": "Tech Innovation News",
                "link": "https://example.com/article2",
                "description": "General tech news without AI focus",
                "published": "2024-01-01T09:00:00Z",
            },
        ]
    )
    return parser


@pytest.fixture
def mock_paywall_bypass():
    """Provide a mock paywall bypass service for testing."""
    bypass = AsyncMock()
    bypass.fetch_content = AsyncMock(
        return_value={
            "success": True,
            "content": "Full article content bypassing paywall...",
            "service_used": "archive.ph",
        }
    )
    return bypass


# Parametrized fixtures for different test scenarios
@pytest.fixture(params=["day", "week", "month"])
def time_periods(request):
    """Provide different time periods for testing."""
    return request.param


@pytest.fixture(params=["positive", "negative", "neutral", "mixed"])
def sentiment_types(request):
    """Provide different sentiment types for testing."""
    return request.param


@pytest.fixture(params=[1, 5, 10, 50])
def article_counts(request):
    """Provide different article counts for testing."""
    return request.param
