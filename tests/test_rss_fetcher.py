from app.fetchers.rss_fetcher import normalize_entry, parse_published_at


def test_parse_published_at_returns_iso_timestamp():
    entry = {"published": "Mon, 01 Jan 2024 00:00:00 GMT"}

    result = parse_published_at(entry)

    assert result == "2024-01-01T00:00:00+00:00"


def test_parse_published_at_returns_none_when_missing():
    result = parse_published_at({})

    assert result is None


def test_normalize_entry_maps_rss_entry_to_article_shape():
    entry = {
        "title": " Test Article ",
        "link": " https://example.com/article ",
        "published": "Mon, 01 Jan 2024 00:00:00 GMT",
        "summary": " Short summary ",
    }
    source = {
        "name": "Example Feed",
        "url": "https://example.com/rss",
        "category": "technology",
        "trust_level": "high",
    }

    article = normalize_entry(entry, source)

    assert article["source_name"] == "Example Feed"
    assert article["source_url"] == "https://example.com/rss"
    assert article["title"] == "Test Article"
    assert article["url"] == "https://example.com/article"
    assert article["published_at"] == "2024-01-01T00:00:00+00:00"
    assert article["raw_summary"] == "Short summary"
    assert article["category_guess"] == "technology"
    assert article["credibility_score"] == 1.0