from app.pipeline.deduplicator import deduplicate_articles


def test_deduplicate_articles_removes_deuplicate_urls():
    articles = [
        {
            "title": "Malaysia AI investment grows",
            "url": "https://example.com/story",
            "relevance_score": 5.0,
        },
        {
            "title": "Different title same URL",
            "url": "https://example.com/story",
            "relevance_score": 3.0,
        },
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 1
    assert result[0]["title"] == "Malaysia AI investment grows"


def test_deduplicate_articles_removes_duplicate_normalized_titles():
    articles =[
        {
            "title": "Malaysia AI Investment Grows!",
            "url": "https://example.com/story-1",
            "relevance_score": 5.0,
        },
        {
            "title": "malaysia ai investment grows",
            "url": "https://example.com/story-2",
            "relevance_score": 4.0,
        },
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 1
    assert result[0]["url"] == "https://example.com/story-1"


def test_deduplicate_articles_keeps_unique_articles():
    articles = [
        {"title": "AI hiring grows", "url": "https://example.com/ai"},
        {"title": "Cybersecurity demand rises", "url": "https://example.com/cyber"},
    ]

    result = deduplicate_articles(articles)

    assert len(result) == 2