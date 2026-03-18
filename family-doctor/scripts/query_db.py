#!/usr/bin/env python3
"""Query helper for family-doctor database."""
import sqlite3
import sys
import os
import json
from datetime import date, datetime, timedelta

DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/family-doctor/medical.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _rows(conn, sql, params=()):
    conn.row_factory = sqlite3.Row
    return [dict(r) for r in conn.execute(sql, params).fetchall()]

# ── Family Members ──

def list_members():
    conn = get_conn()
    rows = _rows(conn, "SELECT * FROM family_members ORDER BY id")
    conn.close()
    return rows

def get_member(member_id=None, name=None):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    if member_id:
        row = conn.execute("SELECT * FROM family_members WHERE id = ?", (member_id,)).fetchone()
    elif name:
        row = conn.execute("SELECT * FROM family_members WHERE name LIKE ?", (f"%{name}%",)).fetchone()
    else:
        return None
    conn.close()
    return dict(row) if row else None

def add_member(**kwargs):
    conn = get_conn()
    cols = [k for k in kwargs if kwargs[k] is not None]
    vals = [kwargs[k] for k in cols]
    sql = f"INSERT INTO family_members ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})"
    c = conn.execute(sql, vals)
    conn.commit()
    mid = c.lastrowid
    conn.close()
    return mid

# ── Medical Records ──

def add_record(**kwargs):
    conn = get_conn()
    cols = [k for k in kwargs if kwargs[k] is not None]
    vals = [kwargs[k] for k in cols]
    sql = f"INSERT INTO medical_records ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})"
    c = conn.execute(sql, vals)
    conn.commit()
    rid = c.lastrowid
    conn.close()
    return rid

def get_records(member_id=None, record_type=None, since=None):
    conn = get_conn()
    sql = """SELECT r.*, m.name as member_name FROM medical_records r
             JOIN family_members m ON r.member_id = m.id WHERE 1=1"""
    params = []
    if member_id:
        sql += " AND r.member_id = ?"; params.append(member_id)
    if record_type:
        sql += " AND r.record_type = ?"; params.append(record_type)
    if since:
        sql += " AND r.record_date >= ?"; params.append(since)
    sql += " ORDER BY r.record_date DESC"
    rows = _rows(conn, sql, params)
    conn.close()
    return rows

def search_records(query, member_id=None):
    conn = get_conn()
    if member_id:
        rows = _rows(conn, """
            SELECT r.*, m.name as member_name FROM medical_records r
            JOIN family_members m ON r.member_id = m.id
            WHERE r.id IN (SELECT rowid FROM medical_records_fts WHERE medical_records_fts MATCH ?)
            AND r.member_id = ? ORDER BY r.record_date DESC
        """, (query, member_id))
    else:
        rows = _rows(conn, """
            SELECT r.*, m.name as member_name FROM medical_records r
            JOIN family_members m ON r.member_id = m.id
            WHERE r.id IN (SELECT rowid FROM medical_records_fts WHERE medical_records_fts MATCH ?)
            ORDER BY r.record_date DESC
        """, (query,))
    conn.close()
    return rows

# ── Medications ──

def add_medication(member_id, drug_name, dose=None, frequency=None, start_date=None, end_date=None, prescribing_record_id=None, notes=None):
    conn = get_conn()
    conn.execute("""INSERT INTO medications (member_id, drug_name, dose, frequency, start_date, end_date, prescribing_record_id, notes)
        VALUES (?,?,?,?,?,?,?,?)""", (member_id, drug_name, dose, frequency, start_date, end_date, prescribing_record_id, notes))
    conn.commit()
    conn.close()

def get_active_medications(member_id):
    conn = get_conn()
    rows = _rows(conn, """SELECT * FROM medications WHERE member_id = ? AND is_active = 1
        AND (end_date IS NULL OR end_date >= date('now')) ORDER BY start_date DESC""", (member_id,))
    conn.close()
    return rows

def stop_medication(medication_id, end_date=None):
    conn = get_conn()
    end_date = end_date or date.today().isoformat()
    conn.execute("UPDATE medications SET is_active = 0, end_date = ? WHERE id = ?", (end_date, medication_id))
    conn.commit()
    conn.close()

# ── Follow-ups ──

def add_followup(member_id, description, due_date, source_record_id=None):
    conn = get_conn()
    conn.execute("INSERT INTO followups (member_id, description, due_date, source_record_id) VALUES (?,?,?,?)",
                 (member_id, description, due_date, source_record_id))
    conn.commit()
    conn.close()

def get_followups(status=None, member_id=None):
    conn = get_conn()
    sql = "SELECT f.*, m.name as member_name FROM followups f JOIN family_members m ON f.member_id = m.id WHERE 1=1"
    params = []
    if status:
        sql += " AND f.status = ?"; params.append(status)
    if member_id:
        sql += " AND f.member_id = ?"; params.append(member_id)
    sql += " ORDER BY f.due_date ASC"
    rows = _rows(conn, sql, params)
    conn.close()
    # Mark overdue
    today = date.today().isoformat()
    for r in rows:
        if r['status'] == 'pending' and r['due_date'] < today:
            r['status'] = 'overdue'
    return rows

def complete_followup(followup_id):
    conn = get_conn()
    conn.execute("UPDATE followups SET status = 'completed', completed_date = date('now') WHERE id = ?", (followup_id,))
    conn.commit()
    conn.close()

# ── Health Metrics ──

def add_metric(member_id, metric_date, metric_name, value, unit=None, reference_range=None, is_abnormal=0, source_record_id=None):
    conn = get_conn()
    conn.execute("""INSERT INTO health_metrics (member_id, metric_date, metric_name, value, unit, reference_range, is_abnormal, source_record_id)
        VALUES (?,?,?,?,?,?,?,?)""", (member_id, metric_date, metric_name, value, unit, reference_range, is_abnormal, source_record_id))
    conn.commit()
    conn.close()

def get_metric_history(member_id, metric_name, since=None):
    conn = get_conn()
    sql = "SELECT * FROM health_metrics WHERE member_id = ? AND metric_name = ?"
    params = [member_id, metric_name]
    if since:
        sql += " AND metric_date >= ?"; params.append(since)
    sql += " ORDER BY metric_date ASC"
    rows = _rows(conn, sql, params)
    conn.close()
    return rows

def get_latest_metrics(member_id):
    conn = get_conn()
    rows = _rows(conn, """SELECT * FROM health_metrics WHERE id IN (
        SELECT MAX(id) FROM health_metrics WHERE member_id = ? GROUP BY metric_name
    ) ORDER BY metric_name""", (member_id,))
    conn.close()
    return rows

# ── Vaccinations ──

def add_vaccination(member_id, vaccine_name, dose_number=None, date_given=None, next_due_date=None, batch_number=None, hospital=None, notes=None):
    conn = get_conn()
    conn.execute("""INSERT INTO vaccinations (member_id, vaccine_name, dose_number, date_given, next_due_date, batch_number, hospital, notes)
        VALUES (?,?,?,?,?,?,?,?)""", (member_id, vaccine_name, dose_number, date_given, next_due_date, batch_number, hospital, notes))
    conn.commit()
    conn.close()

def get_vaccinations(member_id):
    conn = get_conn()
    rows = _rows(conn, "SELECT * FROM vaccinations WHERE member_id = ? ORDER BY date_given DESC", (member_id,))
    conn.close()
    return rows

# ── Growth Records ──

def add_growth_record(member_id, record_date, height_cm=None, weight_kg=None, head_circumference_cm=None, notes=None):
    conn = get_conn()
    conn.execute("""INSERT INTO growth_records (member_id, record_date, height_cm, weight_kg, head_circumference_cm, notes)
        VALUES (?,?,?,?,?,?)""", (member_id, record_date, height_cm, weight_kg, head_circumference_cm, notes))
    conn.commit()
    conn.close()

def get_growth_history(member_id):
    conn = get_conn()
    rows = _rows(conn, "SELECT * FROM growth_records WHERE member_id = ? ORDER BY record_date ASC", (member_id,))
    conn.close()
    return rows

# ── Expenses ──

def add_expense(member_id, date_str, category, amount, description=None, source_record_id=None):
    conn = get_conn()
    conn.execute("INSERT INTO expenses (member_id, date, category, amount, description, source_record_id) VALUES (?,?,?,?,?,?)",
                 (member_id, date_str, category, amount, description, source_record_id))
    conn.commit()
    conn.close()

def get_expense_summary(member_id=None, since=None, until=None):
    conn = get_conn()
    # Combine medical_records.cost and expenses table
    parts = []
    params = []

    base_mr = "SELECT member_id, record_date as date, '就诊' as category, cost as amount, summary as description FROM medical_records WHERE cost IS NOT NULL AND cost > 0"
    base_ex = "SELECT member_id, date, category, amount, description FROM expenses"

    filters_mr, filters_ex = "", ""
    if member_id:
        filters_mr += " AND member_id = ?"; params.append(member_id)
    if since:
        filters_mr += " AND record_date >= ?"; params.append(since)
    if until:
        filters_mr += " AND record_date <= ?"; params.append(until)

    params2 = []
    if member_id:
        filters_ex += " WHERE member_id = ?"; params2.append(member_id)
        if since: filters_ex += " AND date >= ?"; params2.append(since)
        if until: filters_ex += " AND date <= ?"; params2.append(until)
    else:
        if since: filters_ex += " WHERE date >= ?"; params2.append(since)
        if until:
            filters_ex += (" AND" if since else " WHERE") + " date <= ?"; params2.append(until)

    sql = f"""SELECT member_id, date, category, amount, description FROM (
        {base_mr}{filters_mr} UNION ALL {base_ex}{filters_ex}
    ) ORDER BY date DESC"""

    rows = _rows(conn, sql, params + params2)
    conn.close()

    total = sum(r['amount'] for r in rows)
    by_category = {}
    for r in rows:
        by_category[r['category']] = by_category.get(r['category'], 0) + r['amount']
    return {"total": total, "by_category": by_category, "items": rows}


# ── CLI ──

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "list_members"
    if action == "list_members":
        print(json.dumps(list_members(), ensure_ascii=False, indent=2))
    elif action == "search" and len(sys.argv) > 2:
        print(json.dumps(search_records(sys.argv[2]), ensure_ascii=False, indent=2))
    elif action == "records":
        mid = int(sys.argv[2]) if len(sys.argv) > 2 else None
        print(json.dumps(get_records(member_id=mid), ensure_ascii=False, indent=2))
    elif action == "followups":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_followups(status=status), ensure_ascii=False, indent=2))
    elif action == "medications":
        mid = int(sys.argv[2]) if len(sys.argv) > 2 else None
        if mid:
            print(json.dumps(get_active_medications(mid), ensure_ascii=False, indent=2))
    elif action == "metrics":
        mid = int(sys.argv[2])
        name = sys.argv[3] if len(sys.argv) > 3 else None
        if name:
            print(json.dumps(get_metric_history(mid, name), ensure_ascii=False, indent=2))
        else:
            print(json.dumps(get_latest_metrics(mid), ensure_ascii=False, indent=2))
    elif action == "vaccinations":
        mid = int(sys.argv[2])
        print(json.dumps(get_vaccinations(mid), ensure_ascii=False, indent=2))
    elif action == "growth":
        mid = int(sys.argv[2])
        print(json.dumps(get_growth_history(mid), ensure_ascii=False, indent=2))
    elif action == "expenses":
        mid = int(sys.argv[2]) if len(sys.argv) > 2 else None
        since = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(get_expense_summary(member_id=mid, since=since), ensure_ascii=False, indent=2))
    else:
        print("Usage: query_db.py <action> [args]")
        print("Actions: list_members, search, records, followups, medications, metrics, vaccinations, growth, expenses")
