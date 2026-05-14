from app.pipeline.daily_pipeline import run_pipeline_from_articles


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