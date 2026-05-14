from app.db.database import initialize_database
from app.db.repositories import create_source, get_source_by_url, list_sources, create_article, get_article_by_url, list_articles, create_daily_run, complete_daily_run, fail_daily_run, get_daily_run_by_id, create_digest_item, list_digest_items_for_run


def test_create_and_get_source_by_url(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    source = {
        "name": "Example Feed",
        "url": "https://example.com/rss",
        "source_type": "rss",
        "category": "technology",
        "trust_level": "high",
        "is_active": True,
    }

    source_id = create_source(database_path, source)
    saved = get_source_by_url(database_path, "https://example.com/rss")

    assert source_id is not None
    assert saved["name"] == "Example Feed"
    assert saved["url"] == "https://example.com/rss"
    assert saved["is_active"] == 1


def test_list_sources_returns_all_sources(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    create_source(
        database_path,
        {
            "name": "Example Feed",
            "url": "https://example.com/rss",
            "source_type": "rss",
            "category": "technology",
            "trust_level": "high",
            "is_active": True,
        }
    )

    sources = list_sources(database_path)

    assert len(sources) == 1
    assert sources[0]["name"] == "Example Feed"


def test_create_and_get_article_by_url(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    source_id = create_source(
        database_path,
        {
            "name": "Example Feed",
            "url": "https://example.com/rss",
            "source_type": "rss",
            "category": "technology",
            "trust_level": "high",
            "is_active": True,
        },
    )

    article = {
        "source_id": source_id,
        "title": "Malaysia AI hiring grows",
        "url": "https://example.com/article",
        "published_at": "2026-05-14T08:00:00+08:00",
        "raw_summary": "A short RSS summary.",
        "content_text": None,
        "category_guess": "technology",
        "credibility_score": 1.0,
        "freshness_score": None,
        "relevance_score": 4.0,
        "overall_score": 4.0,
        "status": "kept",
        "rejection_reason": None,
    }

    article_id = create_article(database_path, article)
    saved = get_article_by_url(database_path, "https://example.com/article")

    assert article_id is not None
    assert saved["title"] == "Malaysia AI hiring grows"
    assert saved["source_id"] == source_id
    assert saved["status"] == "kept"


def test_list_articles_returns_all_articles(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    create_article(
        database_path,
        {
            "source_id": None,
            "title": "Standalone article",
            "url": "https://example.com/standalone",
            "published_at": None,
            "raw_summary": "",
            "content_text": None,
            "category_guess": "technology",
            "credibility_score": 0.7,
            "freshness_score": None,
            "relevance_score": 2.0,
            "overall_score": 2.0,
            "status": "fetched",
            "rejection_reason": None,
        },
    )

    articles = list_articles(database_path)

    assert len(articles) == 1
    assert articles[0]["title"] == "Standalone article"


def test_create_and_complete_daily_run(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    run_id = create_daily_run(database_path, run_date="2026-05-14")

    complete_daily_run(
        database_path,
        run_id=run_id,
        articles_fetched=10,
        articles_after_filter=8,
        articles_selected=5,
        telegram_sent=False,
    )

    saved = get_daily_run_by_id(database_path, run_id)

    assert saved["run_date"] == "2026-05-14"
    assert saved["status"] == "completed"
    assert saved["articles_fetched"] == 10
    assert saved["articles_after_filter"] == 8
    assert saved["articles_selected"] == 5
    assert saved["telegram_sent"] == 0
    assert saved["completed_at"] is not None


def test_fail_daily_run_records_error_message(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    run_id = create_daily_run(database_path, run_date="2026-05-14")

    fail_daily_run(database_path, run_id=run_id, error_message="RSS fetch failed")

    saved = get_daily_run_by_id(database_path, run_id)

    assert saved["status"] == "failed"
    assert saved["error_message"] == "RSS fetch failed"
    assert saved["completed_at"] is not None


def test_create_and_list_digest_items_for_run(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

    run_id = create_daily_run(database_path, run_date="2026-05-14")
    article_id = create_article(
        database_path,
        {
            "source_id": None,
            "title": "Malaysia AI hiring grows",
            "url": "https://example.com/article",
            "published_at": None,
            "raw_summary": "RSS summary.",
            "content_text": None,
            "category_guess": "technology",
            "credibility_score": 1.0,
            "freshness_score": None,
            "relevance_score": 4.0,
            "overall_score": 4.0,
            "status": "selected",
            "rejection_reason": None,
        },
    )

    digest_item_id = create_digest_item(
        database_path,
        {
            "run_id": run_id,
            "article_id": article_id,
            "rank_position": 1,
            "final_summary": "Short summary for Telegram.",
            "why_it_matters": "Relevant to AI internship preparation.",
            "category": "technology",
            "sent_at": None,
        },
    )

    items = list_digest_items_for_run(database_path, run_id)

    assert digest_item_id is not None
    assert len(items) == 1
    assert items[0]["rank_position"] == 1
    assert items[0]["final_summary"] == "Short summary for Telegram."
    assert items[0]["why_it_matters"] == "Relevant to AI internship preparation."