from typing import Any


def build_article_summary_prompt(
    article: dict[str, Any], profile: dict[str, Any]
) -> str:
    """Build the prompt used to summarise one selected article."""
    interests = ", ".join(profile.get("interests", []))
    career_goals = ", ".join(profile.get("career_goals", []))
    priority_locations = ", ".join(profile.get("priority_locations", []))

    return f"""
        You are summarising one news article for a Computer Science student in Malaysia.

        User profile:
        - Interests: {interests}
        - Career goals: {career_goals}
        - Priority locations: {priority_locations}

        Article:
        - Title: {article.get("title", "")}
        - URL: {article.get("url", "")}
        - Category: {article.get("category_guess", "")}
        - RSS summary: {article.get("raw_summary", "")}
        - Extracted content: {article.get("content_text", "")}

        Return concise JSON with exactly these keys:
        - final_summary: 2-3 plain English sentences.
        - why_it_matters: 1-2 sentences explaining why this matters for the user's goals.

        Do not include unsupported claims. If the article is not relevant, say so briefly.
    """.strip()
