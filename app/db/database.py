from pathlib import Path
import sqlite3

DEFAULT_DATABASE_PATH = Path("data/news_bot.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def get_connection(
    database_path: Path | str = DEFAULT_DATABASE_PATH,
) -> sqlite3.Connection:
    """Open a SQLite connection with project defaults enabled."""
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: Path | str = DEFAULT_DATABASE_PATH) -> None:
    """Create the SQLite database and tables if they do not already exist."""
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection(database_path) as connection:
        connection.executescript(schema_sql)
