from app.pipeline.pre_filter import filter_articles, should_keep_article


def test_should_reject_article_without_title():
    article = {"title": "", "url": "https://example.com/news"}

    keep, reason = should_keep_article(article, excluded_topics=[])

    assert keep is False
    assert reason == "missing_title"


def test_should_reject_article_without_url():
    article = {"title": "Useful news", "url": ""}

    keep, reason = should_keep_article(article, excluded_topics=[])

    assert keep is False
    assert reason == "missing_url"


def test_should_reject_article_matching_excluded_topic():
    article = {
        "title": "Celebrity gossip dominates tech event",
        "url": "https://example.com/news",
        "raw_summary": "A viral entertainment story.",
    }

    keep, reason = should_keep_article(article, excluded_topics=["celebrity gossip"])

    assert keep is False
    assert reason == "excluded_topic"


def test_should_keep_valid_article():
    article = {
        "title": "Malaysia announces new AI investment",
        "url": "https://example.com/news",
        "raw_summary": "The policy may affect local tech hiring",
    }

    keep, reason = should_keep_article(article, excluded_topics=["celebrity gossip"])

    assert keep is True
    assert reason is None


def test_filter_articles_returns_kept_and_rejected_articles():
    articles = [
        {"title": "Useful AI news", "url": "https://example.com/ai", "raw_summary": ""},
        {"title": "", "url": "https://example.com/bad", "raw_summary": ""},
    ]

    kept, rejected = filter_articles(articles, excluded_topics=[])

    assert len(kept) == 1
    assert len(rejected) == 1
    assert rejected[0]["status"] == "rejected"
    assert rejected[0]["rejection_reason"] == "missing_title"
