from typing import Any

import requests


class TelegramSender:
    """Send digest messages through the Telegram Bot API."""

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        http_client: Any = requests,
        max_message_length: int = 4000,
    ) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.http_client = http_client
        self.max_message_length = max_message_length

    def send_message(self, text: str) -> None:
        """Send one Telegram message, splitting when Telegram's limit is approached."""
        for chunk in split_message(text, self.max_message_length):
            self._send_chunk(chunk)

    def _send_chunk(self, text: str) -> None:
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


def split_message(text: str, max_length: int) -> list[str]:
    """Split long Telegram messages on paragraph boundaries when possible."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current = ""

    for paragraph in text.split("\n\n"):
        next_block = paragraph if not current else f"{current}\n\n{paragraph}"

        if len(next_block) <= max_length:
            current = next_block
            continue

        if current:
            chunks.append(current)

        if len(paragraph) <= max_length:
            current = paragraph
        else:
            chunks.extend(
                paragraph[index : index + max_length]
                for index in range(0, len(paragraph), max_length)
            )
            current = ""

    if current:
        chunks.append(current)

    return chunks
