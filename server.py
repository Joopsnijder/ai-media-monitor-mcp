"""AI Media Monitor MCP Server."""

from datetime import datetime
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.ai_media_monitor.core import MediaAnalyzer
from src.ai_media_monitor.models import Article, Expert, TopicSuggestion, TrendingTopic

# Initialize FastMCP server
mcp = FastMCP()

# Initialize analyzer
analyzer = MediaAnalyzer()


@mcp.tool(
    name="scan_media_sources",
    description="Scan all configured Dutch media sources for AI-related articles",
)
async def scan_media_sources(hours_back: int = 24) -> dict[str, Any]:
    """Scan all media sources for recent AI articles"""
    return await analyzer.scan_media_sources(hours_back)


@mcp.tool(
    name="get_trending_topics",
    description="Get trending AI topics in Dutch media with detailed analysis",
)
async def get_trending_topics(
    period: str = "week",
    min_mentions: int = 3,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    """Analyze trending AI topics in Dutch media"""
    # Determine time period
    hours_map = {"day": 24, "week": 168, "month": 720}
    hours = hours_map.get(period, 168)

    # Get articles - use database for weekly reports, RSS for shorter periods
    if hours >= 48:  # Use database for periods longer than 48 hours
        scan_result = await analyzer.get_articles_from_database(hours_back=hours)
    else:
        scan_result = await analyzer.scan_media_sources(hours_back=hours)

    articles = [Article(**a) for a in scan_result["articles"]]

    # Group by topic - assign each article to its most relevant topic only
    topic_articles = {}
    topic_sources = {}
    used_articles = set()  # Track articles already assigned

    def calculate_topic_relevance(article, topic):
        """Calculate how relevant a topic is to an article based on title/content"""
        score = 0
        text = (article.title + (article.summary or "")).lower()

        # Topic-specific scoring
        topic_keywords = {
            "AI en privacy": ["privacy", "gegevens", "persoonlijk", "gdpr", "vertrouwelijk"],
            "generative AI": ["genereren", "creëren", "tekst", "afbeelding", "chatbot", "gpt"],
            "AI in retail": ["winkel", "verkoop", "klant", "e-commerce", "retail"],
            "AI in finance": ["bank", "financieel", "betalen", "krediet", "investering"],
            "AI in de zorg": ["zorg", "patient", "diagnose", "medisch", "ziekenhuis"],
            "AI wetgeving": ["wet", "regel", "europa", "ai act", "compliance"],
            "machine learning": ["leren", "training", "data", "algoritme", "model"]
        }

        keywords = topic_keywords.get(topic, [])
        for keyword in keywords:
            if keyword in text:
                score += 2

        # Base score if topic appears in title
        if topic.lower() in article.title.lower():
            score += 3

        return score

    for article in articles:
        if id(article) in used_articles:
            continue

        # Find the most relevant topic for this article
        best_topic = None
        best_score = 0

        for topic in article.ai_topics:
            if categories and topic not in categories:
                continue

            score = calculate_topic_relevance(article, topic)
            if score > best_score:
                best_score = score
                best_topic = topic

        # If no specific relevance found, use the first topic
        if best_topic is None and article.ai_topics:
            valid_topics = [t for t in article.ai_topics if not categories or t in categories]
            if valid_topics:
                best_topic = valid_topics[0]

        if best_topic:
            if best_topic not in topic_articles:
                topic_articles[best_topic] = []
                topic_sources[best_topic] = set()

            topic_articles[best_topic].append(article)
            topic_sources[best_topic].add(article.source)
            used_articles.add(id(article))

    # Create trending topics
    trending = []
    for topic, articles_list in topic_articles.items():
        if len(articles_list) >= min_mentions:
            # Sort articles by date
            articles_list.sort(key=lambda x: x.date, reverse=True)

            # Determine sentiment (simplified)
            positive_words = ["succes", "doorbraak", "innovatie", "verbetering", "kans"]
            negative_words = ["risico", "gevaar", "probleem", "zorgen", "kritiek"]

            sentiment_score = 0
            for article in articles_list:
                text = (article.title + (article.summary or "")).lower()
                sentiment_score += sum(1 for word in positive_words if word in text)
                sentiment_score -= sum(1 for word in negative_words if word in text)

            sentiment = (
                "positive"
                if sentiment_score > 0
                else "negative"
                if sentiment_score < 0
                else "neutral"
            )

            # Create suggested angle based on content
            if "privacy" in topic.lower():
                angle = "Praktische oplossingen voor privacy-uitdagingen"
            elif "zorg" in topic.lower():
                angle = "Succesverhalen uit Nederlandse ziekenhuizen"
            elif "wetgeving" in topic.lower():
                angle = "Wat betekent nieuwe regelgeving voor jouw organisatie?"
            else:
                angle = f"De realiteit achter {topic} in Nederland"

            trending.append(
                TrendingTopic(
                    topic=topic,
                    mentions=len(articles_list),
                    sources=list(topic_sources[topic]),
                    sentiment=sentiment,
                    key_articles=articles_list[:5],
                    suggested_angle=angle,
                    growth_percentage=None,  # Would need historical data
                )
            )

    # Sort by mentions
    trending.sort(key=lambda x: x.mentions, reverse=True)

    return {"period": period, "topics": [t.dict() for t in trending]}


@mcp.tool(
    name="identify_experts", description="Identify potential podcast guests based on media coverage"
)
async def identify_experts(
    topic: str | None = None, period: str = "month", min_quotes: int = 2
) -> dict[str, Any]:
    """Find experts quoted in Dutch media about AI topics"""
    hours_map = {"week": 168, "month": 720, "quarter": 2160}
    hours = hours_map.get(period, 720)

    # Get articles - use database for longer periods
    if hours >= 48:  # Use database for periods longer than 48 hours
        scan_result = await analyzer.get_articles_from_database(hours_back=hours)
    else:
        scan_result = await analyzer.scan_media_sources(hours_back=hours)

    articles = [Article(**a) for a in scan_result["articles"]]

    # Filter by topic if specified
    if topic:
        articles = [a for a in articles if topic in a.ai_topics]

    # Collect expert information
    expert_data = {}

    for article in articles:
        for expert_quote in article.quoted_experts:
            name = expert_quote["name"]

            if name not in expert_data:
                expert_data[name] = {
                    "quotes": [],
                    "articles": [],
                    "topics": set(),
                    "organizations": [],
                }

            expert_data[name]["quotes"].append(expert_quote["quote"])
            expert_data[name]["articles"].append(article)
            expert_data[name]["topics"].update(article.ai_topics)

            # Try to extract organization from article
            import re

            org_pattern = (
                rf"{name}[,\s]+(?:van|bij|CEO|CTO|directeur|professor|hoogleraar)"
                r"\s+([A-Z][a-zA-Z\s]+)"
            )
            org_match = re.search(org_pattern, article.content or article.summary or "")
            if org_match:
                expert_data[name]["organizations"].append(org_match.group(1))

    # Create Expert objects
    experts = []
    for name, data in expert_data.items():
        if len(data["quotes"]) >= min_quotes:
            # Determine title and organization
            organizations = list(set(data["organizations"]))
            organization = organizations[0] if organizations else None

            # Create contact hints
            contact_hints = []
            if organization:
                contact_hints.append(f"Via {organization}")
            contact_hints.append("LinkedIn zoeken op naam + AI")

            experts.append(
                Expert(
                    name=name,
                    organization=organization,
                    expertise=list(data["topics"]),
                    recent_quotes=len(data["quotes"]),
                    articles=data["articles"][:5],
                    contact_hints=contact_hints,
                )
            )

    # Sort by number of quotes
    experts.sort(key=lambda x: x.recent_quotes, reverse=True)

    return {
        "period": period,
        "topic_filter": topic,
        "experts": [e.dict() for e in experts[:20]],  # Top 20
    }


@mcp.tool(
    name="generate_topic_suggestions",
    description="Generate podcast topic suggestions based on media trends",
)
async def generate_topic_suggestions(
    focus_areas: list[str] | None = None
) -> dict[str, Any]:
    """Generate actionable podcast topic suggestions"""
    # Get recent trends
    trends = await get_trending_topics(period="week", min_mentions=2)
    trending_topics = [TrendingTopic(**t) for t in trends["topics"]]

    # Get experts
    experts_result = await identify_experts(period="month", min_quotes=1)
    available_experts = [Expert(**e) for e in experts_result["experts"]]

    suggestions = []

    for trend in trending_topics[:10]:
        # Skip if not in focus areas
        if focus_areas and not any(area in trend.topic for area in focus_areas):
            continue

        # Find relevant experts
        topic_experts = [
            e for e in available_experts if any(topic in e.expertise for topic in [trend.topic])
        ]

        # Calculate relevance score
        relevance_score = min(10, trend.mentions * 0.5 + len(topic_experts) * 2)

        # Generate questions based on topic
        questions = []
        if "privacy" in trend.topic.lower():
            questions = [
                "Hoe ga je praktisch om met privacy bij AI-implementaties?",
                "Wat zijn de grootste misverstanden over AI en privacy?",
                "Welke concrete stappen moet een organisatie zetten?",
            ]
        elif "zorg" in trend.topic.lower():
            questions = [
                "Wat zijn succesvolle AI-toepassingen in jullie ziekenhuis?",
                "Hoe krijg je artsen mee in AI-innovaties?",
                "Wat zijn de grootste uitdagingen bij AI in de zorg?",
            ]
        elif "wetgeving" in trend.topic.lower():
            questions = [
                "Wat betekent de AI Act concreet voor Nederlandse bedrijven?",
                "Waar moeten organisaties nu al mee beginnen?",
                "Welke sectoren worden het meest geraakt?",
            ]
        else:
            questions = [
                f"Wat is de realiteit van {trend.topic} in Nederland?",
                "Wat zijn de grootste uitdagingen die je tegenkomt?",
                "Welke kansen zie je voor de toekomst?",
            ]

        suggestion = TopicSuggestion(
            topic=trend.topic,
            relevance_score=relevance_score,
            reason=(
                f"{trend.mentions} artikelen deze week, {len(topic_experts)} beschikbare experts"
            ),
            potential_guests=topic_experts[:3],
            unique_angle=trend.suggested_angle or f"Praktijkervaringen met {trend.topic}",
            questions=questions,
        )

        suggestions.append(suggestion)

    # Sort by relevance
    suggestions.sort(key=lambda x: x.relevance_score, reverse=True)

    return {
        "generated_date": datetime.now().isoformat(),
        "suggestions": [s.dict() for s in suggestions],
    }


@mcp.tool(
    name="fetch_article",
    description="Fetch full content of a specific article, bypassing paywall if needed",
)
async def fetch_article(url: str) -> dict[str, Any]:
    """Fetch and analyze a specific article"""
    return await analyzer.fetch_article(url)


@mcp.tool(
    name="get_weekly_report",
    description="Generate a comprehensive weekly report for AIToday Live podcast planning",
)
async def get_weekly_report() -> dict[str, Any]:
    """Generate weekly media monitoring report"""
    # Gather all data
    trends = await get_trending_topics(period="week")
    experts = await identify_experts(period="week", min_quotes=1)
    suggestions = await generate_topic_suggestions()

    # Create summary
    summary = {
        "report_date": datetime.now().isoformat(),
        "week_number": datetime.now().isocalendar()[1],
        "highlights": {
            "top_trending_topic": trends["topics"][0] if trends["topics"] else None,
            "most_quoted_expert": experts["experts"][0] if experts["experts"] else None,
            "best_topic_suggestion": suggestions["suggestions"][0]
            if suggestions["suggestions"]
            else None,
        },
        "statistics": {
            "trending_topics_count": len(trends["topics"]),
            "identified_experts_count": len(experts["experts"]),
            "topic_suggestions_count": len(suggestions["suggestions"]),
        },
        "trends": trends,
        "experts": experts,
        "suggestions": suggestions,
    }

    return summary


# Run the server
if __name__ == "__main__":
    mcp.run()
