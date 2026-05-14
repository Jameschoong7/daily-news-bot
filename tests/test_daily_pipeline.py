from app.pipeline.daily_pipeline import (
    run_persistent_pipeline_from_articles,
    run_pipeline_from_articles,
)

from app.db.database import initialize_database
from app.db.repositories import (
    get_daily_run_by_id,
    list_articles,
    list_digest_items_for_run,
)
from app.ai.provider_base import ArticleSummary


class FakeAIProvider:
    def summarize_article(
        self, article: dict, profile: dict | None = None
    ) -> ArticleSummary:
        return ArticleSummary(
            final_summary=f"AI summary for {article['title']}",
            why_it_matters="AI-generated relevance explanation.",
        )


def test_run_pipeline_from_articles_builds_digest_from_static_articles():
    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai",
            "raw_summary": "Software engineering students may benefit.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        },
        {
            "title": "Celebrity gossip dominates awards show",
            "url": "https://example.com/gossip",
            "raw_summary": "Entertainment story.",
            "source_name": "Example News",
            "category_guess": "entertainment",
            "credibility_score": 0.7,
        },
    ]
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
        "exclude_topics": ["celebrity gossip"],
    }

    result = run_pipeline_from_articles(articles, profile, limit=1)

    assert result["fetched_count"] == 2
    assert result["kept_count"] == 1
    assert result["rejected_count"] == 1
    assert result["selected_count"] == 1
    assert "Malaysia AI internship opportunities grow" in result["digest_text"]
    assert "Celebrity gossip" not in result["digest_text"]


def test_run_persistent_pipeline_from_articles_logs_run_articles_and_digest_items(
    tmp_path,
):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai",
            "raw_summary": "Software engineering students may benefit.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        },
        {
            "title": "Celebrity gossip dominates awards show",
            "url": "https://example.com/gossip",
            "raw_summary": "Entertainment story.",
            "source_name": "Example News",
            "category_guess": "entertainment",
            "credibility_score": 0.7,
        },
    ]
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
        "exclude_topics": ["celebrity gossip"],
    }

    result = run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=articles,
        profile=profile,
        run_date="2026-05-14",
        limit=1,
    )

    saved_run = get_daily_run_by_id(database_path, result["run_id"])
    saved_articles = list_articles(database_path)
    saved_digest_items = list_digest_items_for_run(database_path, result["run_id"])

    assert saved_run["status"] == "completed"
    assert saved_run["articles_fetched"] == 2
    assert saved_run["articles_after_filter"] == 1
    assert saved_run["articles_selected"] == 1

    assert len(saved_articles) == 2
    assert {article["status"] for article in saved_articles} == {"selected", "rejected"}

    assert len(saved_digest_items) == 1
    assert saved_digest_items[0]["rank_position"] == 1
    assert "Malaysia AI internship opportunities grow" in result["digest_text"]


def test_persistent_pipeline_logs_kept_articles_that_are_not_selected(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai-1",
            "raw_summary": "Software engineering students may benefit.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        },
        {
            "title": "Malaysia software engineering hiring grows",
            "url": "https://example.com/ai-2",
            "raw_summary": "Backend internship roles are increasing.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        },
    ]
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
        "exclude_topics": [],
    }

    result = run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=articles,
        profile=profile,
        run_date="2026-05-14",
        limit=1,
    )

    saved_articles = list_articles(database_path)

    assert result["kept_count"] == 2
    assert result["selected_count"] == 1
    assert len(saved_articles) == 2
    assert {article["status"] for article in saved_articles} == {"selected", "kept"}


def test_persistent_pipeline_reuses_existing_article_for_duplicate_url(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai",
            "raw_summary": "Software engineering students may benefit.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        }
    ]
    profile = {
        "interests": ["AI"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
        "exclude_topics": [],
    }

    first_result = run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=articles,
        profile=profile,
        run_date="2026-05-14",
        limit=1,
    )
    second_result = run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=articles,
        profile=profile,
        run_date="2026-05-14",
        limit=1,
    )

    saved_articles = list_articles(database_path)
    first_digest_items = list_digest_items_for_run(
        database_path, first_result["run_id"]
    )
    second_digest_items = list_digest_items_for_run(
        database_path, second_result["run_id"]
    )

    assert len(saved_articles) == 1
    assert len(first_digest_items) == 1
    assert len(second_digest_items) == 1
    assert first_digest_items[0]["article_id"] == saved_articles[0]["id"]
    assert second_digest_items[0]["article_id"] == saved_articles[0]["id"]


def test_persistent_pipeline_uses_ai_provider_for_digest_items(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai",
            "raw_summary": "RSS summary.",
            "source_name": "Example News",
            "category_guess": "technology",
            "credibility_score": 1.0,
        }
    ]
    profile = {
        "interests": ["AI"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
        "exclude_topics": [],
    }

    result = run_persistent_pipeline_from_articles(
        database_path=database_path,
        articles=articles,
        profile=profile,
        run_date="2026-05-14",
        limit=1,
        ai_provider=FakeAIProvider(),
    )

    digest_items = list_digest_items_for_run(database_path, result["run_id"])

    assert digest_items[0]["final_summary"] == (
        "AI summary for Malaysia AI internship opportunities grow"
    )
    assert digest_items[0]["why_it_matters"] == "AI-generated relevance explanation."
    assert (
        "AI summary for Malaysia AI internship opportunities grow"
        in result["digest_text"]
    )
