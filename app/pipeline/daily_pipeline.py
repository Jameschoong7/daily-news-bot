from typing import Any

from app.pipeline.deduplicator import deduplicate_articles
from app.pipeline.digest_builder import build_digest_text, select_top_articles
from app.pipeline.pre_filter import filter_articles
from app.pipeline.relevance_scorer import score_articles


def run_pipeline_from_articles(
    articles: list[dict[str, Any]],
    profile: dict[str, Any],
    limit: int = 5,
) -> dict[str, Any]:
    """Run the non-AI article pipeline on already-fetched articles."""
    excluded_topics = profile.get("exclude_topics", [])

    kept_articles, rejected_articles = filter_articles(
        articles,
        excluded_topics=excluded_topics,
    )
    scored_articles = score_articles(kept_articles, profile)
    unique_articles = deduplicate_articles(scored_articles)
    selected_articles = select_top_articles(unique_articles, limit=limit)
    digest_text = build_digest_text(selected_articles)

    return {
        "fetched_count": len(articles),
        "kept_count": len(kept_articles),
        "rejected_count": len(rejected_articles),
        "selected_count": len(selected_articles),
        "rejected_articles": rejected_articles,
        "selected_articles": selected_articles,
        "digest_text": digest_text,
    }