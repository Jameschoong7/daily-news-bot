from typing import Any
from datetime import date

from app.config.settings import load_environment, load_sources, load_user_profile
from app.fetchers.rss_fetcher import fetch_all_sources
from app.db.database import initialize_database
from app.pipeline.daily_pipeline import run_pipeline_from_articles, run_persistent_pipeline_from_articles

def build_digest_from_inputs(
    sources: list[dict[str, Any]],
    profile: dict[str, Any],
    articles: list[dict[str, Any]] | None = None,
) -> str:
    """Build a non-AI digest from provided articles or configured RSS sources."""
    fetched_articles = articles if articles is not None else fetch_all_sources(sources)
    result = run_pipeline_from_articles(fetched_articles, profile)
    return result["digest_text"]

def build_persistent_digest_from_inputs(
    database_path: str,
    sources: list[dict[str, Any]],
    profile: dict[str, Any],
    articles: list[dict[str, Any]] | None = None,
    run_date: str | None = None,
) -> dict[str, Any]:
    """Build a digest and persist run/article/digest logs."""
    fetched_articles = articles if articles is not None else fetch_all_sources(sources)
    return run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=fetched_articles,
        profile=profile,
        run_date=run_date or date.today().isoformat(),
    )

def main() -> None:
    """Run the local non-AI daily news pipeline, persist logs, and print the digest."""
    environment = load_environment()
    database_path = environment["database_path"] or "data/news_bot.db"

    initialize_database(database_path)

    sources = load_sources()
    profile = load_user_profile()
    result = build_persistent_digest_from_inputs(
        database_path=database_path,
        sources=sources,
        profile=profile,
    )

    print(result["digest_text"])


if __name__ == "__main__":
    main()