# Daily News Bot

A personal Daily News Bot that fetches RSS news, filters and scores articles against a user profile, optionally summarises selected articles with Gemini, sends a Telegram digest, and logs each run in SQLite.

## Purpose

This project is a portfolio-focused automation project for practicing:

- Python backend development
- RSS data ingestion
- rule-based filtering
- explainable relevance scoring
- AI provider abstraction
- SQLite persistence
- Telegram bot delivery
- test-driven development

The bot is designed for personal use, not multi-user SaaS.

## Current MVP Features

- Loads trusted RSS sources from YAML
- Loads a personal relevance profile from YAML
- Fetches RSS article candidates
- Filters invalid or excluded-topic articles
- Scores relevance using an explainable keyword baseline
- Deduplicates repeated articles by URL/title
- Selects top articles for a digest
- Optionally generates final summaries using Gemini
- Falls back to non-AI summaries when no Gemini API key is configured
- Sends Telegram messages when Telegram credentials are configured
- Logs sources, articles, daily runs, and digest items in SQLite
- Includes automated tests for core logic and persistence

## Tech Stack

- Python
- RSS via `feedparser`
- SQLite
- Gemini via `google-genai`
- Telegram Bot API
- APScheduler planned
- Pytest
- Black

## Project Structure

```text
app/
    ai/           AI provider interface, Gemini provider, prompts
    config/       settings, RSS sources, user profile
    db/           SQLite schema, database connection, repositories
    delivery/     Telegram sender
    fetchers/     RSS fetching and article extraction placeholder
    pipeline/     filtering, scoring, deduplication, digest pipeline
    scheduler/    scheduler placeholder
    utils/        utilities placeholder
tests/            unit tests
data/             local SQLite database, ignored by Git
logs/             local logs, ignored by Git
```
## Environment Variables

Create a .env file based on .env.example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
DATABASE_PATH=data/news_bot.db
LOG_LEVEL=INFO
```

All external services are optional for local development:

- Without GEMINI_API_KEY, the bot uses non-AI summaries.
- Without Telegram credentials, the bot prints the digest locally and skips delivery.

## Setup

 ```bash
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
```

## Run Tests

Use the venv-safe command:

```bash
.venv/bin/python -m pytest
```

Format code:

```bash
.venv/bin/python -m black app tests
```

## Run Locally

```bash
.venv/bin/python -m app.main
```

This will:

1. load environment/config files
2. initialize SQLite
3. fetch RSS articles
4. run the filtering/scoring/deduplication pipeline
5. optionally use Gemini summaries
6. persist run/article/digest logs
7. optionally send Telegram message
8. print the final digest

## Pipeline

Load config
Fetch RSS articles
Pre-filter invalid/excluded articles
Score relevance against profile
Deduplicate articles
Select top articles
Generate final summaries
Build digest text
Persist logs
Send Telegram message when configured

## Design Notes

### Swappable AI Provider

The pipeline depends on an AIProvider interface instead of Gemini directly. Gemini is one implementation. This allows a future local model or another provider to be added without rewriting pipeline code.

### Non-AI Fallback

Gemini is optional. If no API key is configured, the bot still produces a digest using RSS summaries and article titles. This keeps the automation reliable and cheap to run.

### Explainable Baseline Scoring

The relevance scorer uses keyword matching from the profile as a simple baseline. It is intentionally explainable before adding more complex semantic scoring.

### Persistence

SQLite stores:

- trusted sources
- fetched article candidates
- daily run logs
- digest items

Repeated article URLs reuse existing article rows to avoid duplicate article records across runs.

## Current Limitations

- Full article extraction is not implemented yet.
- Semantic embeddings are not implemented yet.
- Scheduler is not wired yet.
- Telegram delivery is implemented, but no retry policy yet.
- Gemini failures currently fail the run instead of falling back per article.
- This is single-user only by design.

## Next Steps

- Add scheduler for daily execution
- Add article extraction
- Improve Gemini failure fallback
- Add freshness scoring
- Add semantic relevance scoring
- Add stronger logging

