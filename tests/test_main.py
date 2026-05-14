from app.main import (
    build_ai_provider_from_environment,
    build_digest_from_inputs,
    build_persistent_digest_from_inputs,
    build_telegram_sender_from_environment,
    send_digest_if_configured,
)
from app.db.database import initialize_database
from app.db.repositories import (
    get_daily_run_by_id,
    list_articles,
    list_digest_items_for_run,
)


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


def test_build_persistent_digest_from_inputs_writes_run_logs(tmp_path):
    database_path = tmp_path / "test_news_bot.db"
    initialize_database(database_path)

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

    result = build_persistent_digest_from_inputs(
        database_path=database_path,
        sources=sources,
        profile=profile,
        articles=articles,
        run_date="2026-05-14",
    )

    saved_run = get_daily_run_by_id(database_path, result["run_id"])
    saved_articles = list_articles(database_path)
    saved_digest_items = list_digest_items_for_run(database_path, result["run_id"])

    assert "Malaysia AI startup expands" in result["digest_text"]
    assert saved_run["status"] == "completed"
    assert len(saved_articles) == 1
    assert len(saved_digest_items) == 1


def test_build_ai_provider_returns_none_without_gemini_api_key():
    provider = build_ai_provider_from_environment({"gemini_api_key": None})

    assert provider is None


def test_build_ai_provider_creates_provider_when_gemini_api_key_exists():
    provider = build_ai_provider_from_environment(
        {"gemini_api_key": "fake-key"},
        provider_factory=lambda api_key: f"provider:{api_key}",
    )

    assert provider == "provider:fake-key"


def test_build_telegram_sender_returns_none_without_token_or_chat_id():
    sender = build_telegram_sender_from_environment(
        {
            "telegram_bot_token": None,
            "telegram_chat_id": "12345",
        }
    )

    assert sender is None


def test_build_telegram_sender_creates_sender_when_configured():
    sender = build_telegram_sender_from_environment(
        {
            "telegram_bot_token": "fake-token",
            "telegram_chat_id": "12345",
        },
        sender_factory=lambda bot_token, chat_id: f"sender:{bot_token}:{chat_id}",
    )

    assert sender == "sender:fake-token:12345"


class FakeSender:
    def __init__(self):
        self.messages = []

    def send_message(self, text: str) -> None:
        self.messages.append(text)


def test_send_digest_if_configured_sends_when_sender_exists():
    sender = FakeSender()

    sent = send_digest_if_configured("Digest text", sender)

    assert sent is True
    assert sender.messages == ["Digest text"]


def test_send_digest_if_configured_skips_when_sender_missing():
    sent = send_digest_if_configured("Digest text", sender=None)

    assert sent is False
