#!/usr/bin/env python3
"""Initialize the med-radar SQLite database. Idempotent."""

import sqlite3
import os

DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/med-radar/radar.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            keywords TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'all',
            language_pref TEXT NOT NULL DEFAULT 'both',
            frequency TEXT NOT NULL DEFAULT 'weekly',
            enabled INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS digests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscription_id INTEGER NOT NULL,
            digest_date DATE DEFAULT CURRENT_DATE,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            summary_text TEXT,
            paper_count INTEGER DEFAULT 0,
            key_findings TEXT,
            raw_results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subscription_id) REFERENCES subscriptions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            digest_id INTEGER NOT NULL,
            title TEXT,
            authors TEXT,
            journal TEXT,
            pub_date TEXT,
            doi TEXT,
            url TEXT,
            abstract TEXT,
            ai_summary TEXT,
            relevance_score REAL,
            language TEXT,
            source TEXT,
            FOREIGN KEY (digest_id) REFERENCES digests(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"[OK] Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
