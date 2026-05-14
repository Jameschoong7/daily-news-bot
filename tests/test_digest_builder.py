from app.pipeline.digest_builder import build_digest_text, select_top_articles


def test_select_top_articles_returns_highest_scored_articles():
    articles = [
        {
            "title": "Low score",
            "url": "https://example.com/low",
            "relevance_score": 1.0,
        },
        {
            "title": "High score",
            "url": "https://example.com/high",
            "relevance_score": 5.0,
        },
        {
            "title": "Medium score",
            "url": "https://example.com/medium",
            "relevance_score": 3.0,
        },
    ]

    selected = select_top_articles(articles, limit=2)

    assert [article["title"] for article in selected] == ["High score", "Medium score"]


def test_build_digest_text_formats_articles_for_telegram():
    articles = [
        {
            "title": "Malaysia AI internship opportunities grow",
            "url": "https://example.com/ai",
            "source_name": "Example News",
            "category_guess": "technology",
            "relevance_score": 5.0,
        }
    ]

    digest = build_digest_text(articles)

    assert "Daily News Digest" in digest
    assert "1. Malaysia AI internship opportunities grow" in digest
    assert "Source: Example News" in digest
    assert "Category: technology" in digest
    assert "Score: 5.0" in digest
    assert "https://example.com/ai" in digest


def test_build_digest_text_handles_empty_article_list():
    digest = build_digest_text([])

    assert digest == "No relevant articles found today."
