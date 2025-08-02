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


async def main():
    """Main function to run the MCP client."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Media Monitor MCP Client")
    parser.add_argument(
        "--action",
        choices=["weekly-report", "scan", "trends", "experts"],
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

    args = parser.parse_args()

    client = AIMediaMonitorClient()

    try:
        print("🚀 Starting AI Media Monitor Client...")
        await client.connect()

        if args.action == "weekly-report":
            report_data = await client.generate_weekly_report()
            if report_data:
                await save_report(report_data, args.format)

        elif args.action == "scan":
            scan_data = await client.scan_recent_articles(args.hours)
            if scan_data:
                await save_report(scan_data, args.format)

        elif args.action == "trends":
            trends_data = await client.get_trending_topics_data(args.period)
            if trends_data:
                await save_report(trends_data, args.format)

        elif args.action == "experts":
            experts_data = await client.identify_experts_data(args.period)
            if experts_data:
                await save_report(experts_data, args.format)

        print("✅ Client finished successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
