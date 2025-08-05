"""SQLite database manager for article storage."""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ..models.article import Article


class ArticleDatabase:
    """SQLite database manager for article persistence."""

    def __init__(self, db_path: str = "data/articles.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()

    def _init_database(self) -> None:
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    date_published DATETIME NOT NULL,
                    date_stored DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    content TEXT,
                    summary TEXT,
                    ai_topics TEXT,  -- JSON array
                    quoted_experts TEXT,  -- JSON array
                    mentions_ai BOOLEAN NOT NULL DEFAULT 1
                )
            """)

            # Create indexes for efficient queries
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_date_published ON articles(date_published)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_date_stored ON articles(date_stored)")

    def store_article(self, article: Article) -> bool:
        """Store an article in the database. Returns True if inserted, False if duplicate."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO articles (
                        url, title, source, date_published, content, summary,
                        ai_topics, quoted_experts, mentions_ai
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    article.url,
                    article.title,
                    article.source,
                    article.date.isoformat(),
                    article.content,
                    article.summary,
                    json.dumps(article.ai_topics),
                    json.dumps([
                        expert.model_dump() if hasattr(expert, 'model_dump')
                        else expert.dict() if hasattr(expert, 'dict')
                        else expert if isinstance(expert, dict)
                        else str(expert)
                        for expert in article.quoted_experts
                    ]),
                    article.mentions_ai
                ))
                return True
        except sqlite3.IntegrityError:
            # Article already exists (duplicate URL)
            return False

    def store_articles(self, articles: list[Article]) -> dict[str, int]:
        """Store multiple articles. Returns counts of inserted/duplicate articles."""
        inserted = 0
        duplicates = 0

        for article in articles:
            if self.store_article(article):
                inserted += 1
            else:
                duplicates += 1

        return {"inserted": inserted, "duplicates": duplicates}

    def get_articles_since(self, hours_back: int, sources: list[str] | None = None) -> list[Article]:
        """Get articles from the last N hours, optionally filtered by sources."""
        since_date = datetime.now() - timedelta(hours=hours_back)

        query = """
            SELECT url, title, source, date_published, content, summary,
                   ai_topics, quoted_experts, mentions_ai
            FROM articles 
            WHERE date_published >= ?
        """
        params = [since_date.isoformat()]

        if sources:
            placeholders = ",".join(["?"] * len(sources))
            query += f" AND source IN ({placeholders})"
            params.extend(sources)

        query += " ORDER BY date_published DESC"

        articles = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)

            for row in cursor:
                # Parse JSON fields
                ai_topics = json.loads(row['ai_topics']) if row['ai_topics'] else []
                quoted_experts_data = json.loads(row['quoted_experts']) if row['quoted_experts'] else []

                # Keep expert data as dicts - Article model expects list[dict[str, str]]
                quoted_experts = []
                for expert_data in quoted_experts_data:
                    if isinstance(expert_data, dict):
                        quoted_experts.append(expert_data)
                    elif isinstance(expert_data, str):
                        # Handle string expert data
                        quoted_experts.append({"name": expert_data, "title": "", "organization": ""})
                    # Skip other formats

                article = Article(
                    url=row['url'],
                    title=row['title'],
                    source=row['source'],
                    date=datetime.fromisoformat(row['date_published']),
                    content=row['content'],
                    summary=row['summary'],
                    ai_topics=ai_topics,
                    quoted_experts=quoted_experts,
                    mentions_ai=bool(row['mentions_ai'])
                )
                articles.append(article)

        return articles

    def get_article_count(self, hours_back: int | None = None) -> int:
        """Get total article count, optionally within a time period."""
        query = "SELECT COUNT(*) FROM articles"
        params = []

        if hours_back:
            since_date = datetime.now() - timedelta(hours=hours_back)
            query += " WHERE date_published >= ?"
            params.append(since_date.isoformat())

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()[0]

    def get_sources_stats(self, hours_back: int = 168) -> dict[str, int]:
        """Get article count by source for the given time period."""
        since_date = datetime.now() - timedelta(hours=hours_back)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT source, COUNT(*) as count
                FROM articles 
                WHERE date_published >= ?
                GROUP BY source
                ORDER BY count DESC
            """, [since_date.isoformat()])

            return {row[0]: row[1] for row in cursor}

    def cleanup_old_articles(self, days_to_keep: int = 90) -> int:
        """Remove articles older than specified days. Returns number of deleted articles."""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM articles 
                WHERE date_published < ?
            """, [cutoff_date.isoformat()])

            return cursor.rowcount

    def get_database_info(self) -> dict[str, Any]:
        """Get database statistics and information."""
        with sqlite3.connect(self.db_path) as conn:
            # Total articles
            total_cursor = conn.execute("SELECT COUNT(*) FROM articles")
            total_articles = total_cursor.fetchone()[0]

            # Date range
            date_cursor = conn.execute("""
                SELECT MIN(date_published), MAX(date_published) 
                FROM articles
            """)
            date_range = date_cursor.fetchone()

            # Sources count
            sources_cursor = conn.execute("""
                SELECT source, COUNT(*) as count
                FROM articles
                GROUP BY source
                ORDER BY count DESC
            """)
            sources = {row[0]: row[1] for row in sources_cursor}

            return {
                "database_path": str(self.db_path),
                "total_articles": total_articles,
                "date_range": {
                    "earliest": date_range[0],
                    "latest": date_range[1]
                },
                "sources": sources
            }
