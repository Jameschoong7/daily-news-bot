from typing import Any


def select_top_articles(
    articles: list[dict[str, Any]], limit: int = 5
) -> list[dict[str, Any]]:
    """Select the highest-scored articles for the digest."""
    return sorted(
        articles, key=lambda article: article.get("relevance_score", 0), reverse=True
    )[:limit]


def build_digest_text(articles: list[dict[str, Any]]) -> str:
    """Format selected articles into a Telegram-ready text digest."""
    if not articles:
        return "No relevant articles found today."

    lines = ["Daily News Digest", ""]

    for index, article in enumerate(articles, start=1):
        lines.extend(
            [
                f"{index}. {article.get('title', 'Untitled')}",
                f"Source: {article.get('source_name', 'Unknown')}",
                f"Category: {article.get('category_guess', 'uncategorized')}",
                f"Score: {article.get('relevance_score', 0)}",
                article.get("url", ""),
                "",
            ]
        )

    return "\n".join(lines).strip()
