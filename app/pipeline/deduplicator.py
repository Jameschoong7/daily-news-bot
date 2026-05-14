import re
from typing import Any


def normalize_title(title: str) -> str:
    """Normalize a title so small casing/punctuation changes do not hide duplicates"""
    lowered = title.lower()
    words_only = re.sub(r"[^a-z0-9\s]", "", lowered)
    return " ".join(words_only.split())


def deduplicate_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove articles with duplicate URLs or duplicate normalized titles."""
    seen_urls = set()
    seen_titles = set()
    unique_articles = []

    for article in articles:
        url = article.get("url", "").strip()
        title_key = normalize_title(article.get("title", ""))

        if url and url in seen_urls:
            continue

        if title_key and title_key in seen_titles:
            continue

        if url:
            seen_urls.add(url)

        if title_key:
            seen_titles.add(title_key)

        unique_articles.append(article)

    return unique_articles
