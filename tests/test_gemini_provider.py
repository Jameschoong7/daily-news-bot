from app.ai.gemini_provider import GeminiProvider, parse_summary_response


class FakeResponse:
    text = '{"final_summary": "Short summary.", "why_it_matters": "Useful for internship prep."}'


class FakeModels:
    def generate_content(self, model: str, contents: str):
        self.last_model = model
        self.last_prompt = contents
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


def test_parse_summary_response_returns_article_summary():
    result = parse_summary_response(
        '{"final_summary": "Short summary.", "why_it_matters": "Useful for internship prep."}'
    )

    assert result.final_summary == "Short summary."
    assert result.why_it_matters == "Useful for internship prep."


def test_gemini_provider_uses_model_to_summarize_article():
    client = FakeClient()
    provider = GeminiProvider(client=client)
    article = {
        "title": "Malaysia AI internship opportunities grow",
        "raw_summary": "Software engineering students may benefit.",
    }
    profile = {
        "interests": ["AI"],
        "career_goals": ["internship"],
        "priority_locations": ["Malaysia"],
    }

    result = provider.summarize_article(article, profile)

    assert result.final_summary == "Short summary."
    assert result.why_it_matters == "Useful for internship prep."
    assert "Malaysia AI internship opportunities grow" in client.models.last_prompt


def test_parse_summary_response_handles_markdown_json_fence():
    result = parse_summary_response("""
        ```json
        {
        "final_summary": "Short summary.",
        "why_it_matters": "Useful for internship prep."
        }

        """)
    
    assert result.final_summary == "Short summary."
    assert result.why_it_matters == "Useful for internship prep."


def test_parse_summary_response_handles_text_before_json_object():
    result = parse_summary_response("""
    Here is the JSON:

    {
    "final_summary": "Short summary.",
    "why_it_matters": "Useful for internship prep."
    }
    """)

    assert result.final_summary == "Short summary."
    assert result.why_it_matters == "Useful for internship prep."
