from __future__ import annotations
import feedparser
import hashlib
from datetime import datetime


def parse_rss_feed(url: str, source_name: str) -> list[dict]:
    """Parse an RSS feed and return a list of article dicts."""
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            published = entry.get("published", "")

            if not title or not link:
                continue

            article_id = hashlib.md5(link.encode()).hexdigest()

            articles.append({
                "id": article_id,
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "source": source_name,
                "ai_summary": None,
                "category": None,
                "fetched_at": datetime.utcnow().isoformat(),
            })
        return articles
    except Exception as e:
        print(f"[{source_name}] RSS parse error: {e}")
        return []
