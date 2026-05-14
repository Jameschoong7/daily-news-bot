from app.db.database import initialize_database
from app.db.repositories import create_source, get_source_by_url, list_sources


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
    