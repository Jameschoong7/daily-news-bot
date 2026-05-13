CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    category TEXT,
    trust_level TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TEXT,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_summary TEXT,
    content_text TEXT,
    category_guess TEXT,
    credibility_score REAL,
    freshness_score REAL,
    relevance_score REAL,
    overall_score REAL,
    status TEXT NOT NULL DEFAULT 'fetched',
    rejection_reason TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS daily_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    status TEXT NOT NULL DEFAULT 'running',
    articles_fetched INTEGER NOT NULL DEFAULT 0,
    articles_after_filter INTEGER NOT NULL DEFAULT 0,
    articles_selected INTEGER NOT NULL DEFAULT 0,
    telegram_sent INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS digest_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    rank_position INTEGER NOT NULL,
    final_summary TEXT NOT NULL,
    why_it_matters TEXT NOT NULL,
    category TEXT,
    sent_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES daily_runs(id),
    FOREIGN KEY (article_id) REFERENCES articles(id)
);