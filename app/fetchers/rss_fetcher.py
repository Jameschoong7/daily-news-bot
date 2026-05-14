from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser


def parse_published_at(entry: dict[str, Any]) -> str | None:
    """Convert an RSS published date into an ISO timestamp when available."""
    published = entry.get("published") or entry.get("updated")

    if not published:
        return None

    try:
        parsed = parsedate_to_datetime(published)
    except (TypeError, ValueError):
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.isoformat()


def normalize_entry(entry: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    """Convert one RSS entry into the article shape used by the pipeline."""
    return {
        "source_name": source.get("name"),
        "source_url": source.get("url"),
        "title": entry.get("title", "").strip(),
        "url": entry.get("link", "").strip(),
        "published_at": parse_published_at(entry),
        "raw_summary": entry.get("summary", "").strip(),
        "category_guess": source.get("category"),
        "credibility_score": 1.0 if source.get("trust_level") == "high" else 0.7,
    }


def fetch_rss_source(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch and normalize articles from a single RSS source."""
    parsed_feed = feedparser.parse(source["url"])
    articles = []

    for entry in parsed_feed.entries:
        article = normalize_entry(entry, source)

        if article["title"] and article["url"]:
            articles.append(article)

    return articles


def fetch_all_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Fetch articles from all active RSS sources"""
    articles = []

    for source in sources:
        if not source.get("is_active", True):
            continue

        if source.get("source_type") != "rss":
            continue

        articles.extend(fetch_rss_source(source))

    return articles
