from app.ai.gemini_provider import GeminiProvider, parse_summary_response


class FakeResponse:
    text = '{"final_summary": "Short summary.", "why_it_matters": "Useful for internship prep."}'


class FakeModel:
    def generate_content(self, prompt: str):
        self.last_prompt = prompt
        return FakeResponse()


def test_parse_summary_response_returns_article_summary():
    result = parse_summary_response(
        '{"final_summary": "Short summary.", "why_it_matters": "Useful for internship prep."}'
    )

    assert result.final_summary == "Short summary."
    assert result.why_it_matters == "Useful for internship prep."


def test_gemini_provider_uses_model_to_summarize_article():
    model = FakeModel()
    provider = GeminiProvider(model=model)
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
    assert "Malaysia AI internship opportunities grow" in model.last_prompt
