from app.main import build_digest_from_inputs


def test_build_digest_from_inputs_returns_digest_text():
    sources = []
    profile = {
        "interests": ["AI"],
        "career_goals": [],
        "priority_locations": ["Malaysia"],
        "exclude_topics": [],
    }
    articles = [
        {
            "title": "Malaysia AI startup expands",
            "url": "https://example.com/ai",
            "raw_summary": "AI news.",
            "source_name": "Example News",
            "category_guess": "technology",
        }
    ]

    digest = build_digest_from_inputs(sources, profile, articles=articles)

    assert "Daily News Digest" in digest
    assert "Malaysia AI startup expands" in digest
    