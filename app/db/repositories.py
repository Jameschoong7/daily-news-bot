from pathlib import Path
from typing import Any

from app.db.database import DEFAULT_DATABASE_PATH, get_connection


def row_to_dict(row: Any) -> dict[str, Any] | None:
    """Convert a SQLite row to a plain dict for easier app usage."""
    if row is None:
        return None
    
    return dict(row)


def create_source(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
    source: dict[str, Any] | None = None,
) -> int:
    """Insert one trusted news source and return its database id."""
    if source is None:
        raise ValueError("source is required")
    
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO sources(
                name, url, source_type, category, trust_level, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                source["name"],
                source["url"],
                source["source_type"],
                source.get("category"),
                source["trust_level"],
                1 if source.get("is_active", True) else 0,
            ),
        )
        

        return cursor.lastrowid
    

def get_source_by_url(
    database_path: Path | str,
    url: str,
) -> dict[str, Any] | None:
    """Find a source by RSS URL."""
    with get_connection(database_path) as connection:
        row = connection.execute(
            "SELECT * FROM sources WHERE url = ?",
            (url,),
        ).fetchone()

    return row_to_dict(row)


def list_sources(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
) -> list[dict[str, Any]]:
    """Return all configured sources from the database."""
    with get_connection(database_path) as connection:
        rows = connection.execute(
            "SELECT * FROM sources ORDER BY id"
        ).fetchall()
    
    return [dict(row) for row in rows]


def create_article(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
    article: dict[str, Any] | None = None,
) -> int:
    """Insert one fetched article candidate and return its database id."""
    if article is None:
          raise ValueError("article is required")

    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO articles (
                source_id,
                title,
                url,
                published_at,
                raw_summary,
                content_text,
                category_guess,
                credibility_score,
                freshness_score,
                relevance_score,
                overall_score,
                status,
                rejection_reason
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article.get("source_id"),
                article["title"],
                article["url"],
                article.get("published_at"),
                article.get("raw_summary"),
                article.get("content_text"),
                article.get("category_guess"),
                article.get("credibility_score"),
                article.get("freshness_score"),
                article.get("relevance_score"),
                article.get("overall_score"),
                article.get("status", "fetched"),
                article.get("rejection_reason"),
            ),
        )

        return cursor.lastrowid
    

def get_article_by_url(
    database_path: Path | str,
    url: str,    
) -> dict[str, Any] | None:
    """Find an article by URL."""
    with get_connection(database_path) as connection:
        row = connection.execute(
            "SELECT * FROM articles WHERE url = ?",
            (url,),
        ).fetchone()
    
    return row_to_dict(row)


def list_articles(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
) -> list[dict[str, Any]]:
    """Return all stored articles from the database."""
    with get_connection(database_path) as connection:
        rows = connection.execute(
            "SELECT * FROM articles ORDER BY id"
        ).fetchall()

    return [dict(row) for row in rows]


def create_daily_run(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
    run_date: str | None = None,
) -> int:
    """Create a daily run log row and return its database id."""
    if run_date is None:
        raise ValueError("run_date is required")
    
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO daily_runs (run_date, status)
            VALUES (COALESCE(?, DATE('now')), 'running')
            """,
            (run_date,),
        )

        return cursor.lastrowid
    

def get_daily_run_by_id(
    database_path: Path | str,
    run_id: int,
) -> dict[str, Any] | None:
    """Find a daily run by id."""
    with get_connection(database_path) as connection:
        row = connection.execute(
            "SELECT * FROM daily_runs WHERE id = ?",
            (run_id,),
        ).fetchone()

    return row_to_dict(row)


def complete_daily_run(
    database_path: Path | str,
    run_id: int,
    articles_fetched: int,
    articles_after_filter: int,
    articles_selected: int,
    telegram_sent: bool,
) -> None:
    """Mark a daily run as completed with final article counts."""
    with get_connection(database_path) as connection:
        connection.execute(
            """
            UPDATE daily_runs
            SET
                completed_at = CURRENT_TIMESTAMP,
                status = 'completed',
                articles_fetched = ?,
                articles_after_filter = ?,
                articles_selected = ?,
                telegram_sent = ?,
                error_message = NULL
            WHERE id = ?
            """,
            (
                articles_fetched,
                articles_after_filter,
                articles_selected,
                1 if telegram_sent else 0,
                run_id,
            ),
        )


def fail_daily_run(
    database_path: Path | str,
    run_id: int,
    error_message: str,
) -> None:
    """Mark a daily run as failed and store the error message."""
    with get_connection(database_path) as connection:
        connection.execute(
            """
            UPDATE daily_runs
            SET
                completed_at = CURRENT_TIMESTAMP,
                status = 'failed',
                error_message = ?
            WHERE id = ?
            """,
            (error_message, run_id),
        )