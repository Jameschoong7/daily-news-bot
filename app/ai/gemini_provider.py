import json
from typing import Any

from google import genai

from app.ai.prompts import build_article_summary_prompt
from app.ai.provider_base import AIProvider, ArticleSummary

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


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
        client: Any | None = None,
        model_name: str = DEFAULT_GEMINI_MODEL,
    ) -> None:
        if client is not None:
            self.client = client
        else:
            if api_key is None:
                raise ValueError("api_key is required when client is not provided")

            self.client = genai.Client(api_key=api_key)

        self.model_name = model_name

    def summarize_article(
        self,
        article: dict[str, Any],
        profile: dict[str, Any] | None = None,
    ) -> ArticleSummary:
        """Summarise one article with Gemini."""
        prompt = build_article_summary_prompt(article, profile or {})
        response = self.client.models.generate_content(
            model=self.model_name, contents=prompt
        )

        return parse_summary_response(response.text)
