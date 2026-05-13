from typing import Any

def article_text(article: dict[str, Any]) -> str:
    """Combine article fields used for simple text-based filtering."""
    title = article.get("title", "")
    summary = article.get("raw_summary", "")
    return f"{title} {summary}".lower()


def should_keep_article(
        article: dict[str, Any],
        excluded_topics: list[str],
) -> tuple[bool, str | None]:
    """Decide whether an article passes cheap rule-based filtering."""
    if not article.get("title","").strip():
        return False, "missing_title"
    
    if not article.get("url","").strip():
        return False, "missing_url"
    
    text = article_text(article)

    for topic in excluded_topics:
        if topic.lower() in text:
            return False, "excluded_topic"
        
    return True, None


def filter_articles(
    articles: list[dict[str, Any]],
    excluded_topics: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split articles into kept and rejected lists with rejection reasons."""
    kept = []
    rejected = []

    for article in articles:
        keep, reason = should_keep_article(article, excluded_topics)

        if keep:
            kept.append({**article, "status": "kept", "rejection_reason": None})
        else:
            rejected.append({**article, "status": "rejected", "rejection_reason": reason})

    return kept, rejected