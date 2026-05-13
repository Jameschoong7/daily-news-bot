from typing import Any
import re


TITLE_WEIGHT = 2.0
BODY_WEIGHT = 1.0


def article_text(article: dict[str, Any]) -> tuple[str, str]:
    """Return title text and supporting text used for relevance scoring."""
    title = article.get("title","").lower()
    body = " ".join(
        [
            article.get("raw_summary", ""),
            article.get("category_guess", ""),
        ]
    ).lower()

    return title, body


def profile_keywords(profile: dict[str, Any]) -> list[str]:
    """Collect profile terms that represent User's news interest"""
    keywords = []

    for field in ("interests", "career_goals", "priority_locations"):
        keywords.extend(profile.get(field,[]))

    return [keyword.lower() for keyword in keywords if keyword]


def contains_keyword(text: str, keyword: str) -> bool:
    """Return True when a keyword appears as a whole word or phrase."""
    pattern = rf"\b{re.escape(keyword)}\b"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def score_article(article: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    """Assign a simple explainable relevance score to one article."""
    title, body = article_text(article)
    score = 0.0

    for keyword in profile_keywords(profile):
        if contains_keyword(title, keyword):
            score += TITLE_WEIGHT
        elif contains_keyword(body, keyword):
            score += BODY_WEIGHT
    
    return {**article, "relevance_score":score}


def score_articles(
        articles: list[dict[str, Any]],
        profile: dict[str, Any],
) -> list[dict[str, Any]]:
    """Score articles and return them from most to least relevant."""
    scored_articles = [score_article(article,profile) for article in articles]

    return sorted(
        scored_articles,
        key=lambda article: article["relevance_score"],
        reverse=True
    )