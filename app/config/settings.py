from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import os
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "app" / "config"

SOURCES_PATH = CONFIG_DIR / "sources.yaml"
USER_PROFILE_PATH = CONFIG_DIR / "user_profile.yaml"


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file and return an empty dict when the file is blank."""
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_sources() -> list[dict[str, Any]]:
    """Load active and inactive news source definitions from YAML"""
    data = load_yaml_file(SOURCES_PATH)
    return data.get("sources", [])


def load_user_profile() -> dict[str, Any]:
    """Load the personal relevance profile used by the scoring pipeline."""
    return load_yaml_file(USER_PROFILE_PATH)


def load_environment() -> dict[str, str | None]:
    """Load environment variables needed by external services."""
    load_dotenv()

    return {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "database_path": os.getenv("DATABASE_PATH", "data/news_bot.db"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }