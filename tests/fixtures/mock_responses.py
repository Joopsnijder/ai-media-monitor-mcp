"""Mock HTTP responses for testing web scraping functionality."""

from typing import Any

# Mock RSS feed responses
MOCK_RSS_RESPONSES: dict[str, dict[str, Any]] = {
    "nrc_success": {
        "status_code": 200,
        "headers": {"content-type": "application/rss+xml"},
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>NRC Tech</title>
        <description>Technology news from NRC</description>
        <item>
            <title>AI revolutie in de zorg</title>
            <link>https://www.nrc.nl/nieuws/2024/01/01/ai-zorg</link>
            <description>Nieuwe AI-systemen helpen artsen bij diagnoses</description>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>""",
    },
    "volkskrant_success": {
        "status_code": 200,
        "headers": {"content-type": "application/rss+xml"},
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Volkskrant Tech</title>
        <item>
            <title>Privacy zorgen bij ChatGPT</title>
            <link>https://www.volkskrant.nl/nieuws/2024/01/01/chatgpt-privacy</link>
            <description>Scholen worstelen met privacy-vragen</description>
            <pubDate>Mon, 01 Jan 2024 11:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>""",
    },
    "empty_feed": {
        "status_code": 200,
        "headers": {"content-type": "application/rss+xml"},
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Empty Feed</title>
        <description>No items</description>
    </channel>
</rss>""",
    },
    "invalid_xml": {
        "status_code": 200,
        "headers": {"content-type": "application/rss+xml"},
        "content": "Invalid XML content <invalid>",
    },
    "http_error": {"status_code": 404, "headers": {}, "content": "Not Found"},
    "timeout_error": {"status_code": 408, "headers": {}, "content": "Request Timeout"},
}

# Mock article content responses
MOCK_ARTICLE_RESPONSES: dict[str, dict[str, Any]] = {
    "ai_healthcare_full": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<head><title>AI revolutie in de zorg</title></head>
<body>
    <article>
        <h1>AI revolutie in de zorg</h1>
        <p class="byline">Door Tech Redactie</p>
        <div class="content">
            <p>Nederlandse ziekenhuizen omarmen kunstmatige intelligentie.</p>
            <p>"AI stelt ons in staat om preciezere diagnoses te stellen," 
               zegt Prof. Dr. Marie van der Berg van het Erasmus MC.</p>
            <p>Het LUMC gebruikt AI voor risico-inschatting. Dr. Jan Pieterse 
               legt uit: "We kunnen eerder ingrijpen bij problemen."</p>
        </div>
    </article>
</body>
</html>""",
    },
    "paywalled_article": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<head><title>Premium Article</title></head>
<body>
    <div class="paywall">
        <h1>Subscribe to read this article</h1>
        <p>This content is only available to subscribers.</p>
    </div>
</body>
</html>""",
    },
    "non_ai_article": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<head><title>Sports News</title></head>
<body>
    <article>
        <h1>Football Match Results</h1>
        <p>Ajax won the match against PSV with a score of 2-1.</p>
        <p>The coach was pleased with the team's performance.</p>
    </article>
</body>
</html>""",
    },
    "article_with_experts": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<body>
    <article>
        <h1>AI Ethics Discussion</h1>
        <p>Experts discuss AI ethics in the Netherlands.</p>
        <p>"We need clear guidelines," says Dr. Lisa Janssen from UvA.</p>
        <p>Professor Sarah de Wit from TU Delft adds: "Education is key."</p>
        <p>According to Dr. Ahmed Hassan from UU: "Bias is a real concern."</p>
    </article>
</body>
</html>""",
    },
    "article_http_error": {"status_code": 403, "headers": {}, "content": "Forbidden"},
}

# Mock paywall bypass responses
MOCK_PAYWALL_BYPASS_RESPONSES: dict[str, dict[str, Any]] = {
    "archive_ph_success": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<body>
    <div class="article-content">
        <h1>Full Article Content</h1>
        <p>This is the full article content retrieved via archive.ph.</p>
        <p>"AI is transforming healthcare," says expert Dr. Smith.</p>
    </div>
</body>
</html>""",
    },
    "12ft_io_success": {
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "content": """
<html>
<body>
    <main>
        <h1>Bypassed Article</h1>
        <p>Article content from 12ft.io bypass service.</p>
        <p>Multiple expert quotes and AI-related information.</p>
    </main>
</body>
</html>""",
    },
    "bypass_failed": {
        "status_code": 429,
        "headers": {},
        "content": "Rate limit exceeded",
    },
}

# Mock API responses for testing different scenarios
MOCK_API_RESPONSES: dict[str, dict[str, Any]] = {
    "scan_success_large": {
        "scan_date": "2024-01-01T12:00:00",
        "hours_scanned": 24,
        "total_articles": 50,
        "articles": [
            {
                "title": f"AI Article {i}",
                "url": f"https://example.com/article{i}",
                "source": "NRC" if i % 2 == 0 else "Volkskrant",
                "date": "2024-01-01T10:00:00",
                "summary": f"Article {i} about AI developments",
                "ai_topics": ["AI", "Technology"],
                "quoted_experts": [],
                "mentions_ai": True,
                "content": None,
            }
            for i in range(1, 11)
        ],
        "trending_topics": [
            {"topic": "AI in healthcare", "count": 15},
            {"topic": "AI ethics", "count": 10},
            {"topic": "Machine learning", "count": 8},
        ],
        "potential_guests": [],
    },
    "scan_success_empty": {
        "scan_date": "2024-01-01T12:00:00",
        "hours_scanned": 24,
        "total_articles": 0,
        "articles": [],
        "trending_topics": [],
        "potential_guests": [],
    },
    "scan_success_mixed": {
        "scan_date": "2024-01-01T12:00:00",
        "hours_scanned": 24,
        "total_articles": 5,
        "articles": [
            {
                "title": "AI in Healthcare",
                "url": "https://example.com/ai-health",
                "source": "NRC",
                "date": "2024-01-01T10:00:00",
                "summary": "AI revolutionizes healthcare",
                "ai_topics": ["AI in healthcare"],
                "quoted_experts": [{"name": "Dr. Smith", "quote": "AI helps doctors"}],
                "mentions_ai": True,
                "content": "Full article content...",
            },
            {
                "title": "Privacy Concerns",
                "url": "https://example.com/privacy",
                "source": "Volkskrant",
                "date": "2024-01-01T09:00:00",
                "summary": "Privacy issues with AI",
                "ai_topics": ["AI privacy"],
                "quoted_experts": [{"name": "Prof. Jones", "quote": "Privacy matters"}],
                "mentions_ai": True,
                "content": None,  # Paywalled
            },
        ],
        "trending_topics": [
            {"topic": "AI in healthcare", "count": 3},
            {"topic": "AI privacy", "count": 2},
        ],
        "potential_guests": [
            {"name": "Dr. Smith", "expertise": ["AI in healthcare"]},
            {"name": "Prof. Jones", "expertise": ["AI privacy"]},
        ],
    },
}

# Mock error responses
MOCK_ERROR_RESPONSES: dict[str, dict[str, Any]] = {
    "network_error": {"error": "NetworkError", "message": "Connection failed"},
    "timeout_error": {"error": "TimeoutError", "message": "Request timed out"},
    "parsing_error": {"error": "ParsingError", "message": "Could not parse content"},
    "rate_limit_error": {"error": "RateLimitError", "message": "Rate limit exceeded"},
}

# Mock configuration for different test environments
MOCK_CONFIGS: dict[str, dict[str, Any]] = {
    "minimal": {
        "media_sources": {"newspapers": []},
        "paywall_services": [],
        "retry_attempts": 1,
        "timeout": 10,
        "rate_limit": 5,
    },
    "full_featured": {
        "media_sources": {
            "newspapers": [
                {
                    "name": "NRC",
                    "url": "https://www.nrc.nl",
                    "rss": "https://www.nrc.nl/rss/",
                    "categories": ["tech", "politics"],
                }
            ],
            "tech_media": [
                {
                    "name": "Tweakers",
                    "url": "https://tweakers.net",
                    "rss": "https://feeds.tweakers.net/mixed.xml",
                    "categories": ["tech"],
                }
            ],
        },
        "paywall_services": [
            {"url": "https://archive.ph", "method": "POST", "priority": 1},
            {"url": "https://12ft.io", "method": "GET", "priority": 2},
        ],
        "retry_attempts": 3,
        "timeout": 30,
        "rate_limit": 10,
    },
    "high_performance": {
        "media_sources": {
            "newspapers": [
                {
                    "name": f"Source{i}",
                    "url": f"https://source{i}.com",
                    "rss": f"https://source{i}.com/rss",
                }
                for i in range(1, 21)
            ]
        },
        "paywall_services": [
            {"url": f"https://bypass{i}.com", "method": "GET", "priority": i} for i in range(1, 6)
        ],
        "retry_attempts": 5,
        "timeout": 60,
        "rate_limit": 50,
    },
}
