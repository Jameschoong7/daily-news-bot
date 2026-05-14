from app.delivery.telegram_sender import TelegramSender


class FakeResponse:
    def raise_for_status(self) -> None:
        self.raised = False


class FakeHttpClient:
    def __init__(self):
        self.calls = []

    def post(self, url: str, json: dict, timeout: int):
        self.calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse()


def test_telegram_sender_posts_message_to_bot_api():
    http_client = FakeHttpClient()
    sender = TelegramSender(
        bot_token="fake-token",
        chat_id="12345",
        http_client=http_client,
    )

    sender.send_message("Daily digest text")

    assert len(http_client.calls) == 1
    call = http_client.calls[0]
    assert call["url"] == "https://api.telegram.org/botfake-token/sendMessage"
    assert call["json"] == {
        "chat_id": "12345",
        "text": "Daily digest text",
        "disable_web_page_preview": False,
    }
    assert call["timeout"] == 10


def test_telegram_sender_splits_long_messages():
    http_client = FakeHttpClient()
    sender = TelegramSender(
        bot_token="fake-token",
        chat_id="12345",
        http_client=http_client,
        max_message_length=20,
    )

    sender.send_message("First paragraph.\n\nSecond paragraph.\n\nThird paragraph.")

    assert len(http_client.calls) > 1
    assert all(len(call["json"]["text"]) <= 20 for call in http_client.calls)
