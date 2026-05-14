from typing import Any

import requests


class TelegramSender:
    """Send digest messages through the Telegram Bot API."""

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        http_client: Any = requests,
    ) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.http_client = http_client

    def send_message(self, text: str) -> None:
        """Send one Telegram message."""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        response = self.http_client.post(
            url,
            json={
                "chat_id": self.chat_id,
                "text": text,
                "disable_web_page_preview": False,
            },
            timeout=10,
        )
        response.raise_for_status()
