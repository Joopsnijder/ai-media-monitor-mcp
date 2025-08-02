"""Main media analyzer class."""

import asyncio
from collections import Counter
from datetime import datetime, timedelta
from typing import Any

import aiohttp
import feedparser
from bs4 import BeautifulSoup

from ..models import Article, MediaSource
from ..utils import (
    extract_ai_topics,
    extract_quotes_and_experts,
    fetch_article_content,
    is_ai_related,
)
from .config_loader import load_config


class MediaAnalyzer:
    """Main class for analyzing Dutch media sources."""

    def __init__(self):
        self.config = load_config()

    async def parse_article(
        self, session: aiohttp.ClientSession, item: dict, source_name: str
    ) -> Article | None:
        """Parse RSS item into Article object"""
        try:
            # Extract basic info
            title = item.get("title", "")
            url = item.get("link", "")

            # Skip if not AI-related
            if not is_ai_related(title + item.get("summary", "")):
                return None

            # Parse date
            date_str = item.get("published", item.get("updated", ""))
            try:
                date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            except (ValueError, TypeError):
                date = datetime.now()

            # Fetch full content
            content = await fetch_article_content(session, url)

            # Extract AI topics and experts
            full_text = title + (content or item.get("summary", ""))
            ai_topics = extract_ai_topics(full_text)
            quoted_experts = extract_quotes_and_experts(content) if content else []

            return Article(
                title=title,
                url=url,
                source=source_name,
                date=date,
                content=content[:5000] if content else None,  # Limit content length
                summary=item.get("summary", ""),
                mentions_ai=True,
                ai_topics=ai_topics,
                quoted_experts=quoted_experts,
            )
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None

    async def scan_media_sources(self, hours_back: int = 24) -> dict[str, Any]:
        """Scan all media sources for recent AI articles"""
        articles = []
        since_date = datetime.now() - timedelta(hours=hours_back)

        async with aiohttp.ClientSession() as session:
            for _category, sources in self.config.media_sources.items():
                for source_data in sources:
                    source = MediaSource(**source_data)
                    if not source.rss:
                        continue

                    try:
                        # Fetch RSS feed
                        rss_content = await self._fetch_with_retry(session, source.rss)
                        if not rss_content:
                            continue

                        # Parse feed
                        feed = feedparser.parse(rss_content)

                        # Process entries
                        for entry in feed.entries[:20]:  # Limit to recent 20
                            article = await self.parse_article(session, entry, source.name)
                            if article and article.date >= since_date:
                                articles.append(article)

                        # Rate limiting
                        await asyncio.sleep(0.5)

                    except Exception as e:
                        print(f"Error processing {source.name}: {e}")

        return self._analyze_articles(articles, hours_back)

    async def _fetch_with_retry(
        self, session: aiohttp.ClientSession, url: str, retries: int = 3
    ) -> str | None:
        """Fetch URL with retry logic"""
        for attempt in range(retries):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                if attempt == retries - 1:
                    print(f"Failed to fetch {url}: {e}")
                await asyncio.sleep(2**attempt)  # Exponential backoff
        return None

    def _analyze_articles(self, articles: list[Article], hours_back: int) -> dict[str, Any]:
        """Analyze articles and extract insights"""
        # Extract trending topics
        topic_counter = Counter()
        for article in articles:
            for topic in article.ai_topics:
                topic_counter[topic] += 1

        trending_topics = [
            {"topic": topic, "count": count} for topic, count in topic_counter.most_common(10)
        ]

        # Extract potential guests
        expert_counter = Counter()
        expert_details = {}
        for article in articles:
            for expert in article.quoted_experts:
                name = expert["name"]
                expert_counter[name] += 1
                if name not in expert_details:
                    expert_details[name] = {"quotes": [], "articles": []}
                expert_details[name]["quotes"].append(expert["quote"])
                expert_details[name]["articles"].append(
                    {"title": article.title, "source": article.source, "url": article.url}
                )

        potential_guests = []
        for name, count in expert_counter.most_common(10):
            if count >= 2:  # Mentioned at least twice
                potential_guests.append(
                    {
                        "name": name,
                        "mentions": count,
                        "recent_quotes": expert_details[name]["quotes"][:3],
                        "articles": expert_details[name]["articles"][:3],
                    }
                )

        return {
            "scan_date": datetime.now().isoformat(),
            "hours_scanned": hours_back,
            "total_articles": len(articles),
            "articles": [article.dict() for article in articles[:50]],  # Limit response
            "trending_topics": trending_topics,
            "potential_guests": potential_guests,
        }

    async def fetch_article(self, url: str) -> dict[str, Any]:
        """Fetch and analyze a specific article"""
        async with aiohttp.ClientSession() as session:
            content = await fetch_article_content(session, url)

            if content:
                # Extract metadata
                soup = BeautifulSoup(content, "html.parser")

                # Try to find title
                title = ""
                if soup.find("h1"):
                    title = soup.find("h1").get_text().strip()
                elif soup.find("title"):
                    title = soup.find("title").get_text().strip()

                # Extract text content
                text_content = soup.get_text()

                # Analyze
                is_ai = is_ai_related(text_content)
                topics = extract_ai_topics(text_content) if is_ai else []
                experts = extract_quotes_and_experts(text_content) if is_ai else []

                return {
                    "url": url,
                    "title": title,
                    "content_preview": text_content[:2000],
                    "is_ai_related": is_ai,
                    "ai_topics": topics,
                    "quoted_experts": experts,
                    "fetch_successful": True,
                }
            else:
                return {
                    "url": url,
                    "fetch_successful": False,
                    "error": "Could not fetch article content",
                }
