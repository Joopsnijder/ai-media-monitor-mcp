#!/usr/bin/env python3
"""
AI Media Monitor MCP Client

A client script that connects to the AI Media Monitor MCP server to generate
weekly reports automatically. Can be run manually or scheduled via cron.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles

try:
    from src.ai_media_monitor.utils.email_sender import EmailSender
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("⚠️  Email functionaliteit niet beschikbaar. Installeer met: uv sync --extra email")


class AIMediaMonitorClient:
    """Client for AI Media Monitor MCP server."""

    def __init__(self):
        """Initialize the client."""
        # Import server functions directly
        try:
            from server import (
                generate_topic_suggestions,
                get_trending_topics,
                get_weekly_report,
                identify_experts,
                scan_media_sources,
            )

            self.scan_media_sources = scan_media_sources
            self.get_trending_topics = get_trending_topics
            self.identify_experts = identify_experts
            self.generate_topic_suggestions = generate_topic_suggestions
            self.get_weekly_report = get_weekly_report
        except ImportError as e:
            print(f"Error importing server functions: {e}")
            sys.exit(1)

    async def connect(self):
        """Connect to the server (no-op for direct import)."""
        print("✅ Connected to server (direct import)")

    async def disconnect(self):
        """Disconnect from the server (no-op for direct import)."""
        print("✅ Disconnected from server")

    async def generate_weekly_report(self) -> dict[str, Any]:
        """Generate a comprehensive weekly report."""
        print("🔍 Generating weekly AI media report...")

        try:
            # Call the get_weekly_report function directly
            report_data = await self.get_weekly_report()

            print("✅ Report generated successfully!")
            stats = report_data.get("statistics", {})
            print(f"📊 Found {stats.get('trending_topics_count', 0)} trending topics")
            print(f"👥 Found {stats.get('identified_experts_count', 0)} potential experts")
            print(f"💡 Generated {stats.get('topic_suggestions_count', 0)} topic suggestions")

            return report_data

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return {}

    async def scan_recent_articles(self, hours_back: int = 24) -> dict[str, Any]:
        """Scan for recent AI-related articles."""
        print(f"🔍 Scanning media sources for articles from last {hours_back} hours...")

        try:
            scan_data = await self.scan_media_sources(hours_back=hours_back)
            print(f"✅ Found {scan_data.get('total_articles', 0)} AI-related articles")
            return scan_data

        except Exception as e:
            print(f"❌ Error scanning articles: {e}")
            return {}

    async def get_trending_topics_data(self, period: str = "week") -> dict[str, Any]:
        """Get trending AI topics."""
        print(f"📈 Analyzing trending topics for period: {period}")

        try:
            trends_data = await self.get_trending_topics(period=period, min_mentions=2)
            print(f"✅ Found {len(trends_data.get('topics', []))} trending topics")
            return trends_data

        except Exception as e:
            print(f"❌ Error getting trending topics: {e}")
            return {}

    async def identify_experts_data(self, period: str = "month") -> dict[str, Any]:
        """Identify potential podcast guests."""
        print(f"👥 Identifying potential experts for period: {period}")

        try:
            experts_data = await self.identify_experts(period=period, min_quotes=1)
            print(f"✅ Found {len(experts_data.get('experts', []))} potential experts")
            return experts_data

        except Exception as e:
            print(f"❌ Error identifying experts: {e}")
            return {}

    async def daily_collect_articles(self) -> dict[str, Any]:
        """Collect and store articles in database for daily archival."""
        print("📚 Running daily article collection...")

        try:
            # Import database here to avoid circular imports
            from src.ai_media_monitor.models.article import Article
            from src.ai_media_monitor.storage.database import ArticleDatabase

            # Initialize database
            db = ArticleDatabase()

            # Scan recent articles (last 24 hours to catch any missed articles)
            scan_data = await self.scan_media_sources(hours_back=24)
            articles_data = scan_data.get("articles", [])

            if not articles_data:
                print("ℹ️  No new articles found")
                return {"stored": 0, "duplicates": 0, "total_in_db": db.get_article_count()}

            # The articles_data contains Article objects serialized as dicts
            # For database storage, we need Article objects
            articles = []
            for article_data in articles_data:
                try:
                    # Handle the case where articles are already Article objects or dicts
                    if hasattr(article_data, 'url'):  # It's an Article object
                        articles.append(article_data)
                    else:  # It's a dict, convert to Article
                        articles.append(Article(**article_data))
                except Exception as e:
                    print(f"Warning: Could not process article: {e}")
                    continue

            # Store in database
            result = db.store_articles(articles)

            print(f"✅ Stored {result['inserted']} new articles")
            print(f"ℹ️  Found {result['duplicates']} duplicate articles (skipped)")

            # Get database stats
            total_articles = db.get_article_count()
            sources_stats = db.get_sources_stats(hours_back=168)  # Weekly stats

            print(f"📊 Database now contains {total_articles} total articles")
            print("📈 Articles by source (last 7 days):")
            for source, count in sources_stats.items():
                print(f"   - {source}: {count}")

            return {
                "stored": result["inserted"],
                "duplicates": result["duplicates"],
                "total_in_db": total_articles,
                "sources_stats": sources_stats
            }

        except Exception as e:
            print(f"❌ Error during daily collection: {e}")
            return {"error": str(e)}


def format_report_markdown(report_data: dict) -> str:
    """Format report data as Markdown."""
    if not report_data:
        return "# AI Media Monitor Report\n\n❌ No data available\n"

    md = []
    md.append("# AI Media Monitor - Weekly Report")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("")

    # Summary statistics
    stats = report_data.get("statistics", {})
    md.append("## 📊 Summary")
    md.append(f"- **Trending Topics:** {stats.get('trending_topics_count', 0)}")
    md.append(f"- **Identified Experts:** {stats.get('identified_experts_count', 0)}")
    md.append(f"- **Topic Suggestions:** {stats.get('topic_suggestions_count', 0)}")
    md.append("")

    # Highlights
    highlights = report_data.get("highlights", {})
    if highlights:
        md.append("## 🌟 Highlights")

        top_topic = highlights.get("top_trending_topic")
        if top_topic:
            md.append(f"### Top Trending Topic: {top_topic.get('topic', 'N/A')}")
            md.append(f"- **Mentions:** {top_topic.get('mentions', 0)}")
            md.append(f"- **Sentiment:** {top_topic.get('sentiment', 'neutral')}")
            md.append(f"- **Suggested Angle:** {top_topic.get('suggested_angle', 'N/A')}")
            md.append("")

        top_expert = highlights.get("most_quoted_expert")
        if top_expert:
            md.append(f"### Most Quoted Expert: {top_expert.get('name', 'N/A')}")
            md.append(f"- **Organization:** {top_expert.get('organization', 'N/A')}")
            md.append(f"- **Recent Quotes:** {top_expert.get('recent_quotes', 0)}")
            md.append("")

    # Trending Topics
    trends = report_data.get("trends", {}).get("topics", [])
    if trends:
        md.append("## 📈 Trending Topics")
        for i, topic in enumerate(trends[:5], 1):
            md.append(f"### {i}. {topic.get('topic', 'N/A')}")
            md.append(f"- **Mentions:** {topic.get('mentions', 0)}")
            md.append(f"- **Sources:** {', '.join(topic.get('sources', []))}")
            md.append(f"- **Sentiment:** {topic.get('sentiment', 'neutral')}")

            key_articles = topic.get("key_articles", [])
            if key_articles:
                md.append("- **Key Articles:**")
                for article in key_articles[:3]:
                    title = article.get("title", "N/A")
                    url = article.get("url", "#")
                    source = article.get("source", "N/A")
                    md.append(f"  - [{title}]({url}) - *{source}*")
            md.append("")

    # Expert Recommendations
    experts = report_data.get("experts", {}).get("experts", [])
    if experts:
        md.append("## 👥 Expert Recommendations")
        for i, expert in enumerate(experts[:5], 1):
            md.append(f"### {i}. {expert.get('name', 'N/A')}")
            org = expert.get("organization")
            if org:
                md.append(f"- **Organization:** {org}")

            expertise = expert.get("expertise", [])
            if expertise:
                md.append(f"- **Expertise:** {', '.join(expertise)}")

            md.append(f"- **Recent Quotes:** {expert.get('recent_quotes', 0)}")

            contact_hints = expert.get("contact_hints", [])
            if contact_hints:
                md.append(f"- **Contact:** {', '.join(contact_hints)}")
            md.append("")

    # Topic Suggestions
    suggestions = report_data.get("suggestions", {}).get("suggestions", [])
    if suggestions:
        md.append("## 💡 Podcast Topic Suggestions")
        for i, suggestion in enumerate(suggestions[:5], 1):
            md.append(f"### {i}. {suggestion.get('topic', 'N/A')}")
            md.append(f"- **Relevance Score:** {suggestion.get('relevance_score', 0):.1f}/10")
            md.append(f"- **Reason:** {suggestion.get('reason', 'N/A')}")
            md.append(f"- **Unique Angle:** {suggestion.get('unique_angle', 'N/A')}")

            questions = suggestion.get("questions", [])
            if questions:
                md.append("- **Suggested Questions:**")
                for question in questions:
                    md.append(f"  - {question}")
            md.append("")

    return "\n".join(md)


async def save_report(report_data: dict, format_type: str = "both"):
    """Save report to file(s)."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"ai_media_report_{timestamp}"

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    json_file = None
    md_file = None

    if format_type in ["json", "both"]:
        json_file = reports_dir / f"{base_filename}.json"
        async with aiofiles.open(json_file, "w", encoding="utf-8") as f:
            await f.write(json.dumps(report_data, indent=2, ensure_ascii=False, default=str))
        print(f"📄 JSON report saved: {json_file}")

    if format_type in ["markdown", "both"]:
        md_content = format_report_markdown(report_data)
        md_file = reports_dir / f"{base_filename}.md"
        async with aiofiles.open(md_file, "w", encoding="utf-8") as f:
            await f.write(md_content)
        print(f"📝 Markdown report saved: {md_file}")

    return json_file, md_file


async def send_email_report(report_data: dict, markdown_file: Path = None, json_file: Path = None):
    """Send report via email if configured."""
    if not EMAIL_AVAILABLE:
        print("⚠️  Email functionaliteit niet beschikbaar")
        return False

    try:
        email_sender = EmailSender()

        # Validate configuration
        if not email_sender.validate_config():
            print("❌ Email configuratie ongeldig. Controleer config/email_config.yaml")
            return False

        # Send email
        success = await email_sender.send_report_email(
            report_data=report_data,
            markdown_file=markdown_file,
            json_file=json_file
        )

        return success

    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Kopieer config/email_config.yaml naar je eigen configuratie")
        return False
    except Exception as e:
        print(f"❌ Fout bij versturen email: {e}")
        return False


async def main():
    """Main function to run the MCP client."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Media Monitor MCP Client")
    parser.add_argument(
        "--action",
        choices=["weekly-report", "scan", "trends", "experts", "daily-collect"],
        default="weekly-report",
        help="Action to perform",
    )
    parser.add_argument(
        "--format", choices=["json", "markdown", "both"], default="both", help="Output format"
    )
    parser.add_argument(
        "--hours", type=int, default=24, help="Hours back to scan (for scan action)"
    )
    parser.add_argument(
        "--period",
        choices=["day", "week", "month"],
        default="week",
        help="Period for trends/experts",
    )
    parser.add_argument("--output", help="Output file (optional)")
    parser.add_argument("--email", action="store_true", help="Send report via email")
    parser.add_argument(
        "--email-only", action="store_true", help="Only send email, don't save files"
    )

    args = parser.parse_args()

    client = AIMediaMonitorClient()

    try:
        print("🚀 Starting AI Media Monitor Client...")
        await client.connect()

        json_file = None
        md_file = None
        report_data = None

        if args.action == "weekly-report":
            report_data = await client.generate_weekly_report()
            if report_data:
                if not args.email_only:
                    json_file, md_file = await save_report(report_data, args.format)

        elif args.action == "scan":
            scan_data = await client.scan_recent_articles(args.hours)
            if scan_data:
                report_data = scan_data
                if not args.email_only:
                    json_file, md_file = await save_report(scan_data, args.format)

        elif args.action == "trends":
            trends_data = await client.get_trending_topics_data(args.period)
            if trends_data:
                report_data = trends_data
                if not args.email_only:
                    json_file, md_file = await save_report(trends_data, args.format)

        elif args.action == "experts":
            experts_data = await client.identify_experts_data(args.period)
            if experts_data:
                report_data = experts_data
                if not args.email_only:
                    json_file, md_file = await save_report(experts_data, args.format)

        elif args.action == "daily-collect":
            collection_data = await client.daily_collect_articles()
            if collection_data and not collection_data.get("error"):
                print("✅ Daily collection completed successfully")
            else:
                print("❌ Daily collection failed")

        # Send email if requested
        if (args.email or args.email_only) and report_data:
            print("📧 Versturen email rapport...")
            email_success = await send_email_report(report_data, md_file, json_file)
            if not email_success:
                print("⚠️  Email kon niet worden verzonden, maar rapport is wel opgeslagen")

        print("✅ Client finished successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
