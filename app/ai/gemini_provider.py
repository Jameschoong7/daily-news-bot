import json
from typing import Any

import google.generativeai as genai

from app.ai.prompts import build_article_summary_prompt
from app.ai.provider_base import AIProvider, ArticleSummary

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"


def parse_summary_response(response_text: str) -> ArticleSummary:
    """Parse Gemini JSON response text into an ArticleSummary."""
    data = json.loads(response_text)

    return ArticleSummary(
        final_summary=data["final_summary"],
        why_it_matters=data["why_it_matters"],
    )


class GeminiProvider(AIProvider):
    """Gemini-backed implementation of the AI summarisation provider."""

    def __init__(
        self,
        api_key: str | None = None,
        model: Any | None = None,
        model_name: str = DEFAULT_GEMINI_MODEL,
    ) -> None:
        if model is not None:
            self.model = model
            return

        if api_key is None:
            raise ValueError("api_key is required when model is not provided")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def summarize_article(
        self,
        article: dict[str, Any],
        profile: dict[str, Any] | None = None,
    ) -> ArticleSummary:
        """Summarise one article with Gemini."""
        prompt = build_article_summary_prompt(article, profile or {})
        response = self.model.generate_content(prompt)

        return parse_summary_response(response.text)
