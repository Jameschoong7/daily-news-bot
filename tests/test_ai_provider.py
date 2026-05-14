from app.ai.provider_base import AIProvider, ArticleSummary


class FakeProvider(AIProvider):
    def summarize_article(self, article: dict) -> ArticleSummary:
        return ArticleSummary(
            final_summary=f"Summary: {article['title']}",
            why_it_matters="Relevant to the configured profile.",
        )
    

def test_ai_provider_returns_article_summary_shape():
    provider = FakeProvider()
    article = {"title": "Malaysia AI internship opportunities grow"}

    result = provider.summarize_article(article)

    assert result.final_summary == "Summary: Malaysia AI internship opportunities grow"
    assert result.why_it_matters == "Relevant to the configured profile."