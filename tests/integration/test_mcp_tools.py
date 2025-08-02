"""Integration tests for MCP tools."""

from unittest.mock import MagicMock, patch

import pytest

from server import (
    fetch_article,
    generate_topic_suggestions,
    get_trending_topics,
    get_weekly_report,
    identify_experts,
    scan_media_sources,
)


class TestScanMediaSources:
    """Integration tests for scan_media_sources tool."""

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_scan_media_sources_success(self, mock_scan):
        """Test successful media source scanning."""
        # Mock analyzer response
        mock_scan.return_value = {
            "scan_date": "2024-01-01T12:00:00",
            "hours_scanned": 24,
            "total_articles": 5,
            "articles": [
                {
                    "title": "AI revolutie in de zorg",
                    "url": "https://example.com/article1",
                    "source": "NRC",
                    "date": "2024-01-01T10:00:00",
                    "ai_topics": ["AI in de zorg"],
                    "quoted_experts": [],
                }
            ],
            "trending_topics": [{"topic": "AI in de zorg", "count": 3}],
            "potential_guests": [],
        }

        # Create mock context
        mock_ctx = MagicMock()

        result = await scan_media_sources(mock_ctx, hours_back=24)

        assert result["total_articles"] == 5
        assert len(result["articles"]) == 1
        assert result["articles"][0]["title"] == "AI revolutie in de zorg"
        assert len(result["trending_topics"]) == 1
        mock_scan.assert_called_once_with(24)

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_scan_media_sources_custom_timeframe(self, mock_scan):
        """Test scanning with custom timeframe."""
        mock_scan.return_value = {
            "scan_date": "2024-01-01T12:00:00",
            "hours_scanned": 48,
            "total_articles": 10,
            "articles": [],
            "trending_topics": [],
            "potential_guests": [],
        }

        mock_ctx = MagicMock()
        result = await scan_media_sources(mock_ctx, hours_back=48)

        assert result["hours_scanned"] == 48
        mock_scan.assert_called_once_with(48)


class TestGetTrendingTopics:
    """Integration tests for get_trending_topics tool."""

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_get_trending_topics_week(self, mock_scan):
        """Test getting trending topics for a week."""
        mock_scan.return_value = {
            "articles": [
                {
                    "title": "AI in healthcare",
                    "url": "https://example.com/1",
                    "source": "NRC",
                    "date": "2024-01-01T10:00:00",
                    "summary": "AI helps doctors",
                    "ai_topics": ["AI in de zorg"],
                    "quoted_experts": [],
                    "mentions_ai": True,
                    "content": None,
                },
                {
                    "title": "Privacy concerns",
                    "url": "https://example.com/2",
                    "source": "Volkskrant",
                    "date": "2024-01-01T11:00:00",
                    "summary": "Privacy issues with AI",
                    "ai_topics": ["AI en privacy"],
                    "quoted_experts": [],
                    "mentions_ai": True,
                    "content": None,
                },
            ]
        }

        mock_ctx = MagicMock()
        result = await get_trending_topics(mock_ctx, period="week", min_mentions=1)

        assert result["period"] == "week"
        assert len(result["topics"]) >= 0
        mock_scan.assert_called_once_with(hours_back=168)

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_get_trending_topics_with_categories(self, mock_scan):
        """Test getting trending topics with category filter."""
        mock_scan.return_value = {
            "articles": [
                {
                    "title": "AI in healthcare",
                    "url": "https://example.com/1",
                    "source": "NRC",
                    "date": "2024-01-01T10:00:00",
                    "summary": "AI helps doctors",
                    "ai_topics": ["AI in de zorg"],
                    "quoted_experts": [],
                    "mentions_ai": True,
                    "content": None,
                }
            ]
        }

        mock_ctx = MagicMock()
        result = await get_trending_topics(mock_ctx, period="day", categories=["AI in de zorg"])

        assert result["period"] == "day"
        mock_scan.assert_called_once_with(hours_back=24)


class TestIdentifyExperts:
    """Integration tests for identify_experts tool."""

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_identify_experts_success(self, mock_scan):
        """Test successful expert identification."""
        mock_scan.return_value = {
            "articles": [
                {
                    "title": "AI Expert Interview",
                    "url": "https://example.com/1",
                    "source": "NRC",
                    "date": "2024-01-01T10:00:00",
                    "summary": "Interview with AI expert",
                    "ai_topics": ["AI in de zorg"],
                    "quoted_experts": [{"name": "Dr. Jan de Vries", "quote": "AI is the future"}],
                    "mentions_ai": True,
                    "content": "Dr. Jan de Vries from TU Delft says AI is revolutionary",
                }
            ]
        }

        mock_ctx = MagicMock()
        result = await identify_experts(mock_ctx, period="month", min_quotes=1)

        assert result["period"] == "month"
        assert "experts" in result
        mock_scan.assert_called_once_with(hours_back=720)

    @pytest.mark.asyncio
    @patch("server.analyzer.scan_media_sources")
    async def test_identify_experts_with_topic_filter(self, mock_scan):
        """Test expert identification with topic filter."""
        mock_scan.return_value = {"articles": []}

        mock_ctx = MagicMock()
        result = await identify_experts(mock_ctx, topic="AI in de zorg", period="week")

        assert result["topic_filter"] == "AI in de zorg"
        assert result["period"] == "week"
        mock_scan.assert_called_once_with(hours_back=168)


class TestGenerateTopicSuggestions:
    """Integration tests for generate_topic_suggestions tool."""

    @pytest.mark.asyncio
    @patch("server.identify_experts")
    @patch("server.get_trending_topics")
    async def test_generate_topic_suggestions_success(self, mock_trending, mock_experts):
        """Test successful topic suggestion generation."""
        mock_trending.return_value = {
            "topics": [
                {
                    "topic": "AI in de zorg",
                    "mentions": 5,
                    "sources": ["NRC", "Volkskrant"],
                    "sentiment": "positive",
                    "key_articles": [],
                    "suggested_angle": "Healthcare AI success",
                    "growth_percentage": None,
                }
            ]
        }

        mock_experts.return_value = {
            "experts": [
                {
                    "name": "Dr. Jan de Vries",
                    "organization": "TU Delft",
                    "expertise": ["AI in de zorg"],
                    "recent_quotes": 3,
                    "articles": [],
                    "contact_hints": [],
                }
            ]
        }

        mock_ctx = MagicMock()
        result = await generate_topic_suggestions(mock_ctx)

        assert "suggestions" in result
        assert "generated_date" in result
        mock_trending.assert_called_once()
        mock_experts.assert_called_once()

    @pytest.mark.asyncio
    @patch("server.identify_experts")
    @patch("server.get_trending_topics")
    async def test_generate_topic_suggestions_with_focus(self, mock_trending, mock_experts):
        """Test topic suggestions with focus areas."""
        mock_trending.return_value = {"topics": []}
        mock_experts.return_value = {"experts": []}

        mock_ctx = MagicMock()
        result = await generate_topic_suggestions(mock_ctx, focus_areas=["privacy", "zorg"])

        assert "suggestions" in result
        mock_trending.assert_called_once()
        mock_experts.assert_called_once()


class TestFetchArticle:
    """Integration tests for fetch_article tool."""

    @pytest.mark.asyncio
    @patch("server.analyzer.fetch_article")
    async def test_fetch_article_success(self, mock_fetch):
        """Test successful article fetching."""
        mock_fetch.return_value = {
            "url": "https://example.com/article",
            "title": "AI News Article",
            "content_preview": "This is an article about AI...",
            "is_ai_related": True,
            "ai_topics": ["AI in de zorg"],
            "quoted_experts": [],
            "fetch_successful": True,
        }

        mock_ctx = MagicMock()
        result = await fetch_article(mock_ctx, "https://example.com/article")

        assert result["fetch_successful"] is True
        assert result["title"] == "AI News Article"
        assert result["is_ai_related"] is True
        mock_fetch.assert_called_once_with("https://example.com/article")

    @pytest.mark.asyncio
    @patch("server.analyzer.fetch_article")
    async def test_fetch_article_failure(self, mock_fetch):
        """Test article fetching failure."""
        mock_fetch.return_value = {
            "url": "https://example.com/article",
            "fetch_successful": False,
            "error": "Could not fetch article content",
        }

        mock_ctx = MagicMock()
        result = await fetch_article(mock_ctx, "https://example.com/article")

        assert result["fetch_successful"] is False
        assert "error" in result
        mock_fetch.assert_called_once_with("https://example.com/article")


class TestGetWeeklyReport:
    """Integration tests for get_weekly_report tool."""

    @pytest.mark.asyncio
    @patch("server.generate_topic_suggestions")
    @patch("server.identify_experts")
    @patch("server.get_trending_topics")
    async def test_get_weekly_report_success(self, mock_trending, mock_experts, mock_suggestions):
        """Test successful weekly report generation."""
        mock_trending.return_value = {
            "topics": [
                {
                    "topic": "AI in de zorg",
                    "mentions": 5,
                    "sources": ["NRC"],
                    "sentiment": "positive",
                    "key_articles": [],
                    "suggested_angle": None,
                    "growth_percentage": None,
                }
            ]
        }

        mock_experts.return_value = {
            "experts": [
                {
                    "name": "Dr. Expert",
                    "organization": "University",
                    "expertise": ["AI"],
                    "recent_quotes": 2,
                    "articles": [],
                    "contact_hints": [],
                }
            ]
        }

        mock_suggestions.return_value = {
            "suggestions": [
                {
                    "topic": "AI Healthcare",
                    "relevance_score": 8.0,
                    "reason": "High activity",
                    "potential_guests": [],
                    "unique_angle": "Dutch healthcare AI",
                    "questions": [],
                }
            ]
        }

        mock_ctx = MagicMock()
        result = await get_weekly_report(mock_ctx)

        assert "report_date" in result
        assert "week_number" in result
        assert "highlights" in result
        assert "statistics" in result
        assert "trends" in result
        assert "experts" in result
        assert "suggestions" in result

        # Check statistics
        assert result["statistics"]["trending_topics_count"] == 1
        assert result["statistics"]["identified_experts_count"] == 1
        assert result["statistics"]["topic_suggestions_count"] == 1

        # Check highlights
        assert result["highlights"]["top_trending_topic"] is not None
        assert result["highlights"]["most_quoted_expert"] is not None
        assert result["highlights"]["best_topic_suggestion"] is not None

        mock_trending.assert_called_once()
        mock_experts.assert_called_once()
        mock_suggestions.assert_called_once()

    @pytest.mark.asyncio
    @patch("server.generate_topic_suggestions")
    @patch("server.identify_experts")
    @patch("server.get_trending_topics")
    async def test_get_weekly_report_empty_data(
        self, mock_trending, mock_experts, mock_suggestions
    ):
        """Test weekly report with empty data."""
        mock_trending.return_value = {"topics": []}
        mock_experts.return_value = {"experts": []}
        mock_suggestions.return_value = {"suggestions": []}

        mock_ctx = MagicMock()
        result = await get_weekly_report(mock_ctx)

        assert result["statistics"]["trending_topics_count"] == 0
        assert result["statistics"]["identified_experts_count"] == 0
        assert result["statistics"]["topic_suggestions_count"] == 0

        # Check highlights are None when no data
        assert result["highlights"]["top_trending_topic"] is None
        assert result["highlights"]["most_quoted_expert"] is None
        assert result["highlights"]["best_topic_suggestion"] is None
