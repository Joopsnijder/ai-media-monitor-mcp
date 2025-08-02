# API Documentation

This document describes the MCP (Model Context Protocol) tools available in the AI Media Monitor server.

## Overview

The AI Media Monitor provides 6 main MCP tools for analyzing Dutch media coverage of AI topics. All tools are asynchronous and return structured data suitable for podcast planning and media analysis.

## Tools Reference

### 1. scan_media_sources

Scans all configured Dutch media sources for AI-related articles.

**Function Signature:**
```python
async def scan_media_sources(ctx: Context, hours_back: int = 24) -> dict[str, Any]
```

**Parameters:**
- `hours_back` (int, optional): Number of hours to look back for articles (default: 24)

**Returns:**
```python
{
    "total_articles": int,
    "sources_scanned": int,
    "articles": [
        {
            "title": str,
            "url": str,
            "source": str, 
            "published_date": str,
            "summary": str,
            "ai_topics": list[str],
            "mentions_ai": bool
        }
    ],
    "scan_time": str,
    "errors": list[str]
}
```

**Example Usage:**
```
Scan media sources for AI articles from the last 48 hours
```

**Use Cases:**
- Daily content monitoring
- Identifying breaking AI news
- Source performance analysis

---

### 2. get_trending_topics

Analyzes trending AI topics in Dutch media with detailed metrics.

**Function Signature:**
```python
async def get_trending_topics(
    ctx: Context,
    period: str = "week",
    min_mentions: int = 3,
    categories: list[str] | None = None,
) -> dict[str, list[TrendingTopic]]
```

**Parameters:**
- `period` (str): Time period - "day", "week", or "month" (default: "week")
- `min_mentions` (int): Minimum mentions required for trending status (default: 3)
- `categories` (list[str], optional): Filter by specific topic categories

**Returns:**
```python
{
    "trending": [
        {
            "topic": str,
            "mentions": int,
            "growth_rate": float,
            "sentiment_score": float,
            "sources": list[str],
            "sample_articles": list[Article],
            "suggested_angle": str | None
        }
    ],
    "period_analyzed": str,
    "total_topics": int
}
```

**TrendingTopic Model:**
- `topic`: AI topic name (e.g., "AI in de zorg")
- `mentions`: Number of articles mentioning this topic
- `growth_rate`: Percentage change from previous period
- `sentiment_score`: Average sentiment (-1.0 to 1.0)
- `sources`: Media sources covering this topic
- `sample_articles`: Representative articles
- `suggested_angle`: Suggested podcast angle

**Example Usage:**
```
Get trending AI topics for the last week with at least 5 mentions
```

---

### 3. identify_experts

Identifies potential podcast guests based on media coverage and expert quotes.

**Function Signature:**
```python
async def identify_experts(
    ctx: Context, 
    topic: str | None = None, 
    period: str = "month", 
    min_quotes: int = 2
) -> dict[str, list[Expert]]
```

**Parameters:**
- `topic` (str, optional): Focus on specific AI topic
- `period` (str): Time period to analyze (default: "month")  
- `min_quotes` (int): Minimum quotes required (default: 2)

**Returns:**
```python
{
    "experts": [
        {
            "name": str,
            "quote_count": int,
            "topics": list[str],
            "recent_quotes": list[dict],
            "sources": list[str],
            "expertise_areas": list[str],
            "contact_potential": str
        }
    ],
    "total_experts": int,
    "analysis_period": str
}
```

**Expert Model:**
- `name`: Expert's full name
- `quote_count`: Number of times quoted
- `topics`: AI topics they've discussed
- `recent_quotes`: Recent quote texts and contexts
- `sources`: Media sources that quoted them
- `expertise_areas`: Inferred areas of expertise
- `contact_potential`: Assessment of how contactable they might be

**Example Usage:**
```
Find AI experts in healthcare who have been quoted at least 3 times this month
```

---

### 4. generate_topic_suggestions

Generates podcast topic suggestions based on current media trends.

**Function Signature:**
```python
async def generate_topic_suggestions(
    ctx: Context, 
    focus_areas: list[str] | None = None
) -> dict[str, list[TopicSuggestion]]
```

**Parameters:**
- `focus_areas` (list[str], optional): Specific areas to focus suggestions on

**Returns:**
```python
{
    "suggestions": [
        {
            "topic": str,
            "relevance_score": float,
            "reason": str,
            "potential_guests": list[str],
            "unique_angle": str,
            "supporting_articles": list[Article]
        }
    ],
    "generated_at": str,
    "focus_areas": list[str]
}
```

**TopicSuggestion Model:**
- `topic`: Suggested podcast topic
- `relevance_score`: Relevance score (0.0 to 1.0)
- `reason`: Why this topic is suggested
- `potential_guests`: Suggested expert guests
- `unique_angle`: Unique angle or approach
- `supporting_articles`: Articles supporting the suggestion

**Example Usage:**
```
Generate podcast topic suggestions focusing on AI ethics and privacy
```

---

### 5. fetch_article

Fetches full content of a specific article, attempting paywall bypass.

**Function Signature:**
```python
async def fetch_article(ctx: Context, url: str) -> dict[str, Any]
```

**Parameters:**
- `url` (str): URL of the article to fetch

**Returns:**
```python
{
    "url": str,
    "title": str,
    "content": str,
    "author": str | None,
    "published_date": str | None,
    "ai_topics": list[str],
    "mentions_ai": bool,
    "experts_quoted": list[dict],
    "fetch_method": str,
    "success": bool,
    "error": str | None
}
```

**Response Fields:**
- `content`: Full article text content
- `fetch_method`: How content was retrieved ("direct", "archive", etc.)
- `experts_quoted`: Extracted expert quotes and attributions
- `success`: Whether fetch was successful
- `error`: Error message if fetch failed

**Example Usage:**
```
Fetch the full content of this NRC article about AI in healthcare
```

---

### 6. get_weekly_report

Generates a comprehensive weekly report for podcast planning.

**Function Signature:**
```python
async def get_weekly_report(ctx: Context) -> dict[str, Any]
```

**Parameters:**
None (analyzes the past week automatically)

**Returns:**
```python
{
    "report_period": str,
    "summary": {
        "total_articles": int,
        "trending_topics_count": int,
        "identified_experts": int,
        "top_sources": list[str]
    },
    "trending_topics": list[TrendingTopic],
    "expert_suggestions": list[Expert],
    "topic_suggestions": list[TopicSuggestion],
    "weekly_highlights": list[str],
    "source_analysis": dict,
    "generated_at": str
}
```

**Report Sections:**
- `summary`: Key metrics overview
- `trending_topics`: Top trending AI topics
- `expert_suggestions`: Recommended podcast guests
- `topic_suggestions`: Suggested episode topics
- `weekly_highlights`: Notable developments
- `source_analysis`: Media source coverage analysis

**Example Usage:**
```
Generate a comprehensive weekly report for podcast planning
```

## Data Models

### Article
```python
class Article(BaseModel):
    title: str
    url: str
    source: str
    published_date: datetime
    summary: str
    content: str = ""
    ai_topics: list[str] = []
    mentions_ai: bool = False
```

### Expert
```python
class Expert(BaseModel):
    name: str
    quote_count: int
    topics: list[str]
    recent_quotes: list[dict[str, str]]
    sources: list[str]
    articles: list[Article] = []
```

### TrendingTopic
```python
class TrendingTopic(BaseModel):
    topic: str
    mentions: int
    growth_rate: float
    sentiment_score: float
    sources: list[str]
    sample_articles: list[Article]
    suggested_angle: str | None = None
```

### TopicSuggestion
```python
class TopicSuggestion(BaseModel):
    topic: str
    relevance_score: float
    reason: str
    potential_guests: list[str]
    unique_angle: str
    supporting_articles: list[Article]
```

## Error Handling

All tools handle errors gracefully and return structured error information:

```python
{
    "success": bool,
    "error": str | None,
    "partial_results": dict | None  # If some data was retrieved
}
```

**Common Error Types:**
- Network connectivity issues
- RSS feed parsing errors
- Paywall bypass failures
- Rate limiting responses
- Invalid configuration

## Rate Limiting

The server implements rate limiting to respect media source servers:

- **Default**: 10 concurrent requests
- **Timeout**: 30 seconds per request
- **Retry**: 3 attempts with exponential backoff

Configure in `config.yaml`:
```yaml
rate_limit: 10
timeout: 30
retry_attempts: 3
```

## Authentication

MCP tools require Context but no additional authentication. Security should be handled at the MCP transport layer.

## Usage Patterns

### Daily Monitoring
```
1. scan_media_sources(hours_back=24)
2. get_trending_topics(period="day")
3. identify_experts(period="day")
```

### Weekly Planning
```
1. get_weekly_report()
2. generate_topic_suggestions()
3. fetch_article(url="...") for detailed analysis
```

### Topic Research
```
1. get_trending_topics(categories=["AI in de zorg"])
2. identify_experts(topic="AI in de zorg")
3. generate_topic_suggestions(focus_areas=["healthcare"])
```

## Best Practices

1. **Batch Requests**: Use weekly report for comprehensive analysis
2. **Filter Results**: Use min_mentions and categories to focus results
3. **Cache Results**: Avoid repeated calls for same time periods
4. **Handle Errors**: Check success flags and error messages
5. **Respect Limits**: Don't exceed rate limiting configuration

## Integration Examples

### Claude Desktop Integration
```json
{
  "mcpServers": {
    "ai-media-monitor": {
      "command": "uv",
      "args": ["run", "server"],
      "cwd": "/path/to/ai-media-monitor-mcp"
    }
  }
}
```

### Custom Client Integration
```python
import asyncio
from mcp import ClientSession

async def analyze_ai_trends():
    async with ClientSession() as session:
        # Scan recent articles
        result = await session.call_tool(
            "scan_media_sources", 
            {"hours_back": 48}
        )
        
        # Get trending topics
        trends = await session.call_tool(
            "get_trending_topics",
            {"period": "week", "min_mentions": 5}
        )
        
        return result, trends
```

## Performance Considerations

- **Concurrent Requests**: Limited by rate_limit setting
- **Memory Usage**: Scales with article retention period
- **Network Usage**: Depends on number of sources and update frequency
- **Cache Efficiency**: Results cached for repeated queries

## Debugging

Enable debug mode for detailed logging:

```python
# Check tool availability
tools = await session.list_tools()
print([tool.name for tool in tools])

# Test individual tools
result = await session.call_tool("scan_media_sources", {"hours_back": 1})
print(f"Success: {result.get('success', False)}")
```