#!/usr/bin/env python3
"""Family Doctor - Charts & Visualization"""

import os
import sys
import sqlite3
import argparse
from datetime import datetime, date
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore', message='Glyph .* missing from current font')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/family-doctor/medical.db")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/data/family-doctor/charts")

# WHO percentile data: months 0,1,2,3,6,9,12,15,18,21,24,27,30,33,36
WHO_MONTHS = [0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

WHO_DATA = {
    'boys': {
        'height': {
            'P3':  [46.1, 51.1, 54.4, 57.3, 63.3, 67.5, 71.0, 74.1, 76.9, 79.4, 81.7, 83.9, 85.9, 87.8, 89.7],
            'P15': [47.9, 52.8, 56.3, 59.3, 65.4, 69.7, 73.3, 76.4, 79.3, 81.7, 84.2, 86.4, 88.4, 90.3, 92.2],
            'P50': [49.9, 54.7, 58.4, 61.4, 67.6, 72.0, 75.7, 78.9, 81.7, 84.2, 86.8, 89.1, 91.1, 93.0, 94.9],
            'P85': [51.8, 56.7, 60.4, 63.5, 69.8, 74.2, 78.0, 81.3, 84.1, 86.7, 89.3, 91.7, 93.8, 95.7, 97.6],
            'P97': [53.4, 58.2, 62.0, 65.2, 71.6, 76.0, 79.9, 83.2, 86.1, 88.7, 91.4, 93.8, 96.0, 97.9, 99.9],
        },
        'weight': {
            'P3':  [2.5, 3.4, 4.3, 5.0, 6.4, 7.4, 8.0, 8.5, 8.9, 9.3, 9.7, 10.0, 10.4, 10.7, 11.0],
            'P15': [2.9, 3.9, 4.9, 5.7, 7.1, 8.2, 8.9, 9.5, 9.9, 10.3, 10.8, 11.2, 11.5, 11.9, 12.2],
            'P50': [3.3, 4.5, 5.6, 6.4, 7.9, 9.2, 9.9, 10.5, 11.0, 11.5, 12.0, 12.4, 12.9, 13.3, 13.7],
            'P85': [3.9, 5.1, 6.3, 7.2, 8.8, 10.2, 11.0, 11.7, 12.2, 12.7, 13.3, 13.8, 14.3, 14.8, 15.3],
            'P97': [4.4, 5.7, 7.0, 7.9, 9.6, 11.1, 12.0, 12.7, 13.3, 13.8, 14.5, 15.1, 15.7, 16.2, 16.8],
        },
    },
    'girls': {
        'height': {
            'P3':  [45.4, 50.0, 53.0, 55.6, 61.2, 65.3, 69.0, 72.0, 74.5, 76.8, 79.0, 81.1, 83.1, 84.9, 86.8],
            'P15': [47.2, 51.8, 55.0, 57.7, 63.4, 67.7, 71.4, 74.4, 77.0, 79.4, 81.7, 83.8, 85.8, 87.7, 89.6],
            'P50': [49.1, 53.7, 57.1, 59.8, 65.7, 70.1, 73.9, 77.0, 79.6, 82.0, 84.3, 86.6, 88.6, 90.5, 92.4],
            'P85': [51.0, 55.6, 59.1, 62.0, 68.0, 72.6, 76.4, 79.5, 82.2, 84.6, 87.0, 89.3, 91.4, 93.3, 95.2],
            'P97': [52.5, 57.1, 60.8, 63.7, 69.8, 74.5, 78.4, 81.6, 84.3, 86.8, 89.2, 91.6, 93.7, 95.7, 97.5],
        },
        'weight': {
            'P3':  [2.4, 3.2, 3.9, 4.5, 5.8, 6.7, 7.3, 7.8, 8.2, 8.6, 9.0, 9.3, 9.7, 10.0, 10.3],
            'P15': [2.8, 3.6, 4.5, 5.2, 6.5, 7.5, 8.2, 8.7, 9.2, 9.6, 10.0, 10.4, 10.8, 11.2, 11.5],
            'P50': [3.2, 4.2, 5.1, 5.8, 7.3, 8.5, 9.2, 9.8, 10.3, 10.8, 11.3, 11.7, 12.2, 12.6, 13.0],
            'P85': [3.7, 4.8, 5.8, 6.6, 8.2, 9.5, 10.3, 11.0, 11.5, 12.1, 12.6, 13.1, 13.7, 14.1, 14.6],
            'P97': [4.2, 5.4, 6.5, 7.4, 9.0, 10.4, 11.3, 12.0, 12.6, 13.2, 13.9, 14.4, 15.0, 15.6, 16.1],
        },
    },
}

def _get_conn():
    return sqlite3.connect(DB_PATH)

def _ensure_dir(path):
    os.makedirs(os.path.dirname(path) if not os.path.isdir(path) else path, exist_ok=True)

def _default_path(name):
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    return os.path.join(DEFAULT_OUTPUT_DIR, name)


def growth_chart(member_id, output_path=None):
    """Growth chart with WHO percentile bands."""
    conn = _get_conn()
    c = conn.cursor()

    # Get member info
    c.execute("SELECT name, gender, birthday FROM family_members WHERE id=?", (member_id,))
    row = c.fetchone()
    if not row:
        print(f"Member {member_id} not found"); return None
    name, gender, birthday = row
    if not birthday:
        print(f"No birthday for {name}"); return None

    birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    gender_key = 'boys' if gender == 'male' else 'girls'

    # Get growth data
    c.execute("SELECT record_date, height_cm, weight_kg FROM growth_records WHERE member_id=? ORDER BY record_date", (member_id,))
    records = c.fetchall()
    conn.close()

    if not records:
        print(f"No growth records for {name}"); return None

    # Calculate age in months
    ages, heights, weights = [], [], []
    for rec_date, h, w in records:
        rd = datetime.strptime(rec_date, "%Y-%m-%d").date()
        age_months = (rd.year - birth_date.year) * 12 + (rd.month - birth_date.month) + (rd.day - birth_date.day) / 30.0
        ages.append(age_months)
        heights.append(h)
        weights.append(w)

    if not output_path:
        output_path = _default_path(f"growth_{member_id}.png")
    _ensure_dir(os.path.dirname(output_path))

    who = WHO_DATA[gender_key]
    months = WHO_MONTHS
    band_colors = ['#e0e0e0', '#c0c0c0', '#a0a0a0', '#c0c0c0', '#e0e0e0']
    percentiles = ['P3', 'P15', 'P50', 'P85', 'P97']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"Growth Chart - {name} ({'Boy' if gender_key == 'boys' else 'Girl'})", fontsize=14)

    for metric, ax, unit, data_y in [('height', ax1, 'cm', heights), ('weight', ax2, 'kg', weights)]:
        # Draw WHO bands
        for i in range(len(percentiles) - 1):
            ax.fill_between(months, who[metric][percentiles[i]], who[metric][percentiles[i+1]],
                          alpha=0.3, color=band_colors[i], label=f'{percentiles[i]}-{percentiles[i+1]}' if i == 0 else None)
        # Draw P50 line
        ax.plot(months, who[metric]['P50'], 'b--', alpha=0.5, linewidth=1, label='P50')
        # Draw P3 and P97 lines
        ax.plot(months, who[metric]['P3'], 'gray', alpha=0.4, linewidth=0.8, linestyle=':')
        ax.plot(months, who[metric]['P97'], 'gray', alpha=0.4, linewidth=0.8, linestyle=':')
        # Child's data
        valid = [(a, v) for a, v in zip(ages, data_y) if v is not None]
        if valid:
            va, vv = zip(*valid)
            ax.plot(va, vv, 'r-o', linewidth=2, markersize=4, label=name)
        ax.set_ylabel(f'{metric.title()} ({unit})')
        ax.legend(loc='lower right', fontsize=8)
        ax.grid(True, alpha=0.3)

    ax2.set_xlabel('Age (months)')
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return output_path


def metric_trend(member_id, metric_name, output_path=None):
    """Single health metric trend over time."""
    conn = _get_conn()
    c = conn.cursor()

    c.execute("SELECT name FROM family_members WHERE id=?", (member_id,))
    row = c.fetchone()
    if not row:
        print(f"Member {member_id} not found"); return None
    name = row[0]

    c.execute("""SELECT metric_date, value, unit, reference_range, is_abnormal
                 FROM health_metrics WHERE member_id=? AND metric_name=?
                 ORDER BY metric_date""", (member_id, metric_name))
    records = c.fetchall()
    conn.close()

    if not records:
        print(f"No {metric_name} data for {name}"); return None

    dates, values, abnormals = [], [], []
    ref_low, ref_high = None, None
    unit = ''
    for rec_date, val, u, ref_range, is_abn in records:
        try:
            v = float(val)
        except (ValueError, TypeError):
            continue
        dates.append(datetime.strptime(rec_date, "%Y-%m-%d").date())
        values.append(v)
        abnormals.append(bool(is_abn))
        if u: unit = u
        if ref_range and '-' in str(ref_range):
            try:
                parts = str(ref_range).split('-')
                ref_low, ref_high = float(parts[0]), float(parts[1])
            except (ValueError, IndexError):
                pass

    if not dates:
        print(f"No numeric {metric_name} data for {name}"); return None

    if not output_path:
        output_path = _default_path(f"metric_{member_id}_{metric_name}.png")
    _ensure_dir(os.path.dirname(output_path))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, values, 'b-o', markersize=5, label=metric_name)

    # Flag abnormal values
    abn_dates = [d for d, a in zip(dates, abnormals) if a]
    abn_vals = [v for v, a in zip(values, abnormals) if a]
    if abn_dates:
        ax.scatter(abn_dates, abn_vals, c='red', s=80, zorder=5, label='Abnormal')

    # Reference range
    if ref_low is not None and ref_high is not None:
        ax.axhspan(ref_low, ref_high, alpha=0.15, color='green', label=f'Ref: {ref_low}-{ref_high}')

    ax.set_title(f"{name} - {metric_name}")
    ax.set_ylabel(f'{metric_name} ({unit})' if unit else metric_name)
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return output_path


def expense_summary(output_path=None, member_id=None, since=None):
    """Medical expense summary charts."""
    conn = _get_conn()
    c = conn.cursor()

    where, params = [], []
    if member_id:
        where.append("e.member_id=?"); params.append(member_id)
    if since:
        where.append("e.date>=?"); params.append(since)
    where_clause = " WHERE " + " AND ".join(where) if where else ""

    # By member
    c.execute(f"""SELECT f.name, SUM(e.amount) FROM expenses e
                  JOIN family_members f ON e.member_id=f.id
                  {where_clause} GROUP BY f.name""", params)
    by_member = c.fetchall()

    # By category
    c.execute(f"""SELECT e.category, SUM(e.amount) FROM expenses e
                  {where_clause.replace('e.member_id', 'e.member_id')} GROUP BY e.category""", params)
    by_cat = c.fetchall()
    conn.close()

    if not by_member and not by_cat:
        print("No expense data found"); return None

    if not output_path:
        output_path = _default_path("expenses.png")
    _ensure_dir(os.path.dirname(output_path))

    n_plots = (1 if by_member else 0) + (1 if by_cat else 0)
    if n_plots == 0:
        print("No expense data"); return None

    fig, axes = plt.subplots(1, n_plots, figsize=(6 * n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    idx = 0
    if by_member:
        names, amounts = zip(*by_member)
        axes[idx].bar(names, amounts, color='steelblue')
        axes[idx].set_title('Expenses by Member')
        axes[idx].set_ylabel('Amount (CNY)')
        idx += 1

    if by_cat:
        cats, amounts = zip(*by_cat)
        axes[idx].bar(cats, amounts, color='coral')
        axes[idx].set_title('Expenses by Category')
        axes[idx].set_ylabel('Amount (CNY)')
        axes[idx].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return output_path


def visit_timeline(output_path=None, member_id=None):
    """Timeline of all medical visits."""
    conn = _get_conn()
    c = conn.cursor()

    if member_id:
        c.execute("""SELECT r.record_date, f.name, r.diagnosis, r.department
                     FROM medical_records r JOIN family_members f ON r.member_id=f.id
                     WHERE r.member_id=? ORDER BY r.record_date""", (member_id,))
    else:
        c.execute("""SELECT r.record_date, f.name, r.diagnosis, r.department
                     FROM medical_records r JOIN family_members f ON r.member_id=f.id
                     ORDER BY r.record_date""")
    records = c.fetchall()
    conn.close()

    if not records:
        print("No visit records found"); return None

    if not output_path:
        output_path = _default_path("timeline.png")
    _ensure_dir(os.path.dirname(output_path))

    # Assign colors per member
    members = list(set(r[1] for r in records))
    colors = plt.cm.Set2(np.linspace(0, 1, max(len(members), 1)))
    color_map = {m: colors[i] for i, m in enumerate(members)}

    fig, ax = plt.subplots(figsize=(12, max(3, len(records) * 0.4)))

    for i, (rec_date, name, diag, dept) in enumerate(records):
        d = datetime.strptime(rec_date, "%Y-%m-%d").date()
        label = f"{diag or dept or 'Visit'}"
        if len(label) > 40:
            label = label[:37] + "..."
        ax.barh(i, 1, left=mdates.date2num(d), height=0.6, color=color_map[name], alpha=0.8)
        ax.text(mdates.date2num(d) + 1, i, f" {name}: {label}", va='center', fontsize=8)

    ax.set_yticks([])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    fig.autofmt_xdate()
    ax.set_title('Medical Visit Timeline')
    ax.grid(True, axis='x', alpha=0.3)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color_map[m], label=m) for m in members]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Family Doctor Charts')
    sub = parser.add_subparsers(dest='command')

    p_growth = sub.add_parser('growth')
    p_growth.add_argument('member_id', type=int)
    p_growth.add_argument('output_path', nargs='?')

    p_metric = sub.add_parser('metric')
    p_metric.add_argument('member_id', type=int)
    p_metric.add_argument('metric_name')
    p_metric.add_argument('output_path', nargs='?')

    p_exp = sub.add_parser('expenses')
    p_exp.add_argument('--member', type=int)
    p_exp.add_argument('--since')
    p_exp.add_argument('output_path', nargs='?')

    p_tl = sub.add_parser('timeline')
    p_tl.add_argument('--member', type=int)
    p_tl.add_argument('output_path', nargs='?')

    args = parser.parse_args()

    if args.command == 'growth':
        growth_chart(args.member_id, args.output_path)
    elif args.command == 'metric':
        metric_trend(args.member_id, args.metric_name, args.output_path)
    elif args.command == 'expenses':
        expense_summary(args.output_path, args.member, args.since)
    elif args.command == 'timeline':
        visit_timeline(args.output_path, args.member)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
