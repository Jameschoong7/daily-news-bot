from typing import Any

from app.config.settings import load_sources, load_user_profile
from app.fetchers.rss_fetcher import fetch_all_sources
from app.pipeline.daily_pipeline import run_pipeline_from_articles


def build_digest_from_inputs(
    sources: list[dict[str, Any]],
    profile: dict[str, Any],
    articles: list[dict[str, Any]] | None = None,
) -> str:
    """Build a non-AI digest from provided articles or configured RSS sources."""
    fetched_articles = articles if articles is not None else fetch_all_sources(sources)
    result = run_pipeline_from_articles(fetched_articles, profile)
    return result["digest_text"]


def main() -> None:
    """Run the local non-AI daiily news pipeline and print the digest."""
    sources = load_sources()
    profile = load_user_profile()
    digest_text = build_digest_from_inputs(sources, profile)

    print(digest_text)


if __name__ == "__main__":
    main()