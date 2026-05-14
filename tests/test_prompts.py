from app.ai.prompts import build_article_summary_prompt


def test_build_article_summary_prompt_includes_article_fields_and_profile():
    article = {
        "title": "Malaysia AI internship opportunities grow",
        "url": "https://example.com/ai",
        "raw_summary": "Software engineering students may benefit.",
        "category_guess": "technology",
    }
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["Backend internship"],
        "priority_locations": ["Malaysia"],
    }

    prompt = build_article_summary_prompt(article, profile)

    assert "Malaysia AI internship opportunities grow" in prompt
    assert "Software engineering students may benefit." in prompt
    assert "AI" in prompt
    assert "Backend internship" in prompt
    assert "final_summary" in prompt
    assert "why_it_matters" in prompt
