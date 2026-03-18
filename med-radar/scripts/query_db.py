#!/usr/bin/env python3
"""Query and manage the med-radar database."""

import sqlite3
import sys
import json
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/med-radar/radar.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def list_subscriptions():
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM subscriptions WHERE enabled = 1 ORDER BY created_at DESC").fetchall()
    conn.close()
    if not rows:
        print("No active subscriptions.")
        return []
    results = []
    for r in rows:
        d = dict(r)
        results.append(d)
        print(f"[{d['id']}] {d['topic']} | keywords: {d['keywords']} | source: {d['source']} | freq: {d['frequency']}")
    return results

def add_subscription(topic, keywords, source='all', language_pref='both', frequency='weekly'):
    conn = get_conn()
    conn.execute(
        "INSERT INTO subscriptions (topic, keywords, source, language_pref, frequency) VALUES (?, ?, ?, ?, ?)",
        (topic, keywords, source, language_pref, frequency)
    )
    conn.commit()
    sub_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(f"[OK] Added subscription #{sub_id}: {topic}")
    return sub_id

def remove_subscription(sub_id):
    conn = get_conn()
    conn.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()
    print(f"[OK] Removed subscription #{sub_id}")

def toggle_subscription(sub_id, enabled):
    conn = get_conn()
    conn.execute("UPDATE subscriptions SET enabled = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (int(enabled), sub_id))
    conn.commit()
    conn.close()
    print(f"[OK] Subscription #{sub_id} {'enabled' if enabled else 'disabled'}")

def get_latest_digest(sub_id):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM digests WHERE subscription_id = ? ORDER BY created_at DESC LIMIT 1", (sub_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return d
    print(f"No digests for subscription #{sub_id}")
    return None

def list_digests(sub_id, limit=10):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, digest_date, period_start, period_end, paper_count, key_findings FROM digests WHERE subscription_id = ? ORDER BY created_at DESC LIMIT ?", (sub_id, limit)).fetchall()
    conn.close()
    results = [dict(r) for r in rows]
    for d in results:
        print(f"[{d['id']}] {d['digest_date']} | {d['period_start']}~{d['period_end']} | {d['paper_count']} papers")
    return results

def save_digest(sub_id, period_start, period_end, summary, paper_count, key_findings, raw_results):
    conn = get_conn()
    conn.execute(
        "INSERT INTO digests (subscription_id, period_start, period_end, summary_text, paper_count, key_findings, raw_results) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sub_id, period_start, period_end, summary, paper_count, key_findings, json.dumps(raw_results, ensure_ascii=False))
    )
    conn.commit()
    digest_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return digest_id

def save_paper(digest_id, **kwargs):
    conn = get_conn()
    cols = ['digest_id'] + list(kwargs.keys())
    vals = [digest_id] + list(kwargs.values())
    placeholders = ','.join(['?'] * len(vals))
    conn.execute(f"INSERT INTO papers ({','.join(cols)}) VALUES ({placeholders})", vals)
    conn.commit()
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: query_db.py <command> [args]")
        print("Commands: list, add, remove, toggle, digests, latest")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_subscriptions()
    elif cmd == "add":
        topic = sys.argv[2]
        keywords = ""
        source = "all"
        lang = "both"
        freq = "weekly"
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--keywords" and i + 1 < len(sys.argv):
                keywords = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--source" and i + 1 < len(sys.argv):
                source = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--lang" and i + 1 < len(sys.argv):
                lang = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--freq" and i + 1 < len(sys.argv):
                freq = sys.argv[i + 1]; i += 2
            else:
                i += 1
        add_subscription(topic, keywords, source, lang, freq)
    elif cmd == "remove":
        remove_subscription(int(sys.argv[2]))
    elif cmd == "toggle":
        toggle_subscription(int(sys.argv[2]), sys.argv[3].lower() in ('1', 'true', 'on'))
    elif cmd == "digests":
        list_digests(int(sys.argv[2]))
    elif cmd == "latest":
        get_latest_digest(int(sys.argv[2]))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
