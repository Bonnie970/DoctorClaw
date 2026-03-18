#!/usr/bin/env python3
"""Initialize the family-doctor SQLite database. Idempotent — safe to re-run."""
import sqlite3
import sys
import os

def init_db(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # --- Original tables ---

    c.execute("""
    CREATE TABLE IF NOT EXISTS family_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        relationship TEXT NOT NULL,
        birthday TEXT,
        gender TEXT,
        blood_type TEXT,
        allergies TEXT,
        chronic_conditions TEXT,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        record_date TEXT NOT NULL,
        record_type TEXT NOT NULL,
        hospital TEXT,
        department TEXT,
        doctor TEXT,
        diagnosis TEXT,
        symptoms TEXT,
        medications TEXT,
        lab_results TEXT,
        raw_ocr_text TEXT,
        summary TEXT,
        source_file TEXT,
        tags TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        note_date TEXT DEFAULT (date('now')),
        category TEXT,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id)
    )
    """)

    # FTS index
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS medical_records_fts USING fts5(
        diagnosis, symptoms, medications, lab_results, raw_ocr_text, summary, tags,
        content='medical_records',
        content_rowid='id'
    )
    """)

    # FTS triggers
    c.executescript("""
    CREATE TRIGGER IF NOT EXISTS medical_records_ai AFTER INSERT ON medical_records BEGIN
        INSERT INTO medical_records_fts(rowid, diagnosis, symptoms, medications, lab_results, raw_ocr_text, summary, tags)
        VALUES (new.id, new.diagnosis, new.symptoms, new.medications, new.lab_results, new.raw_ocr_text, new.summary, new.tags);
    END;
    CREATE TRIGGER IF NOT EXISTS medical_records_ad AFTER DELETE ON medical_records BEGIN
        INSERT INTO medical_records_fts(medical_records_fts, rowid, diagnosis, symptoms, medications, lab_results, raw_ocr_text, summary, tags)
        VALUES ('delete', old.id, old.diagnosis, old.symptoms, old.medications, old.lab_results, old.raw_ocr_text, old.summary, old.tags);
    END;
    CREATE TRIGGER IF NOT EXISTS medical_records_au AFTER UPDATE ON medical_records BEGIN
        INSERT INTO medical_records_fts(medical_records_fts, rowid, diagnosis, symptoms, medications, lab_results, raw_ocr_text, summary, tags)
        VALUES ('delete', old.id, old.diagnosis, old.symptoms, old.medications, old.lab_results, old.raw_ocr_text, old.summary, old.tags);
        INSERT INTO medical_records_fts(rowid, diagnosis, symptoms, medications, lab_results, raw_ocr_text, summary, tags)
        VALUES (new.id, new.diagnosis, new.symptoms, new.medications, new.lab_results, new.raw_ocr_text, new.summary, new.tags);
    END;
    """)

    # --- Migration: add cost column to medical_records ---
    try:
        c.execute("ALTER TABLE medical_records ADD COLUMN cost REAL")
    except sqlite3.OperationalError:
        pass  # column already exists

    # --- New tables (v2) ---

    c.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        drug_name TEXT NOT NULL,
        dose TEXT,
        frequency TEXT,
        start_date TEXT,
        end_date TEXT,
        prescribing_record_id INTEGER,
        is_active INTEGER DEFAULT 1,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id),
        FOREIGN KEY (prescribing_record_id) REFERENCES medical_records(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        due_date TEXT NOT NULL,
        source_record_id INTEGER,
        status TEXT DEFAULT 'pending',
        completed_date TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id),
        FOREIGN KEY (source_record_id) REFERENCES medical_records(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        metric_date TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT,
        reference_range TEXT,
        is_abnormal INTEGER DEFAULT 0,
        source_record_id INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id),
        FOREIGN KEY (source_record_id) REFERENCES medical_records(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS vaccinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        vaccine_name TEXT NOT NULL,
        dose_number INTEGER,
        date_given TEXT,
        next_due_date TEXT,
        batch_number TEXT,
        hospital TEXT,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS growth_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        record_date TEXT NOT NULL,
        height_cm REAL,
        weight_kg REAL,
        head_circumference_cm REAL,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        source_record_id INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (member_id) REFERENCES family_members(id),
        FOREIGN KEY (source_record_id) REFERENCES medical_records(id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.openclaw/workspace/data/family-doctor/medical.db")
    init_db(db_path)
