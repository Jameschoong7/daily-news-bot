from typing import Any
from pathlib import Path

from app.pipeline.deduplicator import deduplicate_articles
from app.pipeline.digest_builder import build_digest_text, select_top_articles
from app.pipeline.pre_filter import filter_articles
from app.pipeline.relevance_scorer import score_articles
from app.db.repositories import (
    complete_daily_run,
    create_article,
    create_daily_run,
    create_digest_item,
    fail_daily_run,
    get_article_by_url,
)


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
        "kept_articles": unique_articles,
        "selected_articles": selected_articles,
        "digest_text": digest_text,
    }


def run_persistent_pipeline_from_articles(
    database_path: Path | str,
    articles: list[dict[str, Any]],
    profile: dict[str, Any],
    run_date: str,
    limit: int = 5,
) -> dict[str, Any]:
    """Run the non-AI pipeline and persist run/article/digest logs."""
    run_id = create_daily_run(database_path, run_date=run_date)

    try:
        result = run_pipeline_from_articles(articles, profile, limit=limit)
        selected_urls = {article.get("url") for article in result["selected_articles"]}

        article_ids_by_url = {}

        for article in result["rejected_articles"]:
            article_id = persist_article_candidate(
                database_path, article, status="rejected"
            )
            article_ids_by_url[article["url"]] = article_id

        for article in result["kept_articles"]:
            article_status = (
                "selected" if article.get("url") in selected_urls else "kept"
            )
            article_id = persist_article_candidate(
                database_path, article, status=article_status
            )
            article_ids_by_url[article["url"]] = article_id

        for rank, article in enumerate(result["selected_articles"], start=1):
            create_digest_item(
                database_path,
                {
                    "run_id": run_id,
                    "article_id": article_ids_by_url[article["url"]],
                    "rank_position": rank,
                    "final_summary": article.get("raw_summary") or article["title"],
                    "why_it_matters": "Matched the configured relevance profile.",
                    "category": article.get("category_guess"),
                    "sent_at": None,
                },
            )

        complete_daily_run(
            database_path,
            run_id=run_id,
            articles_fetched=result["fetched_count"],
            articles_after_filter=result["kept_count"],
            articles_selected=result["selected_count"],
            telegram_sent=False,
        )

        return {**result, "run_id": run_id}

    except Exception as error:
        fail_daily_run(database_path, run_id=run_id, error_message=str(error))
        raise


def persist_article_candidate(
    database_path: Path | str,
    article: dict[str, Any],
    status: str,
) -> int:
    """Create an article row or reuse the existing row for the same URL."""
    existing_article = get_article_by_url(database_path, article["url"])

    if existing_article is not None:
        return existing_article["id"]

    return create_article(
        database_path,
        {
            **article,
            "status": status,
            "overall_score": article.get("relevance_score"),
        },
    )
