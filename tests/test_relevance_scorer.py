from app.pipeline.relevance_scorer import score_article, score_articles


def test_score_article_gives_higher_score_for_profile_match():
    article = {
        "title": "Malaysia AI companies expand internship hiring",
        "raw_summary": "New backend and software engineering roles are opening.",
        "category_guess": "technology",
    }
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["Backend internship"],
        "priority_locations": ["Malaysia"],
    }

    scored = score_article(article, profile)

    assert scored["relevance_score"] > 0


def test_score_article_gives_zero_for_no_profile_match():
    article = {
        "title": "Movie awards ceremony announces nominees",
        "raw_summary": "Entertainment industry celebrities attended the event.",
        "category_guess": "entertainment",
    }
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["Backend internship"],
        "priority_locations": ["Malaysia"],
    }

    scored = score_article(article, profile)

    assert scored["relevance_score"] == 0


def test_score_articles_sorts_highest_relevance_first():
    articles = [
        {
            "title": "Movie awards ceremony",
            "raw_summary": "Entertainment news.",
            "category_guess": "entertainment",
        },
        {
            "title": "Malaysia AI internship opportunities grow",
            "raw_summary": "Software engineering students may benefit.",
            "category_guess": "technology",
        }
    ]
    profile = {
        "interests": ["AI", "software engineering"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
    }

    scored = score_articles(articles, profile)

    assert scored[0]["title"] == "Malaysia AI internship opportunities grow"
    assert scored[0]["relevance_score"] > scored[1]["relevance_score"]