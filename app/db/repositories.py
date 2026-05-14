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