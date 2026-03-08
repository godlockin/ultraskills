#!/usr/bin/env python3
"""
AI 使用量统计 CLI 工具
直接从 SQLite 数据库读取并输出统计信息
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import argparse

DB_PATH = Path(__file__).parent / "ai_usage.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_date_range(period: str) -> tuple:
    today = datetime.now().date()

    if period == 'daily':
        start = end = today
    elif period == 'weekly':
        start = today - timedelta(days=today.weekday())
        end = today
    elif period == 'monthly':
        start = today.replace(day=1)
        end = today
    elif period == 'quarterly':
        quarter = (today.month - 1) // 3
        start = today.replace(month=quarter * 3 + 1, day=1)
        end = today
    elif period == 'yearly':
        start = today.replace(month=1, day=1)
        end = today
    elif period == 'all':
        start = datetime.min.date()
        end = today
    else:
        start = end = today

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def cmd_summary(args):
    """显示汇总统计"""
    start_date, end_date = get_date_range(args.period)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 总体汇总
    cursor.execute('''
        SELECT SUM(total_tokens) as total_tokens,
               SUM(credits) as credits,
               COUNT(DISTINCT date) as days
        FROM daily_usage
        WHERE date BETWEEN ? AND ?
    ''', (start_date, end_date))
    row = cursor.fetchone()

    print(f"\n📊 AI 使用量统计 ({args.period})")
    print("=" * 50)
    print(f"日期范围：{start_date} ~ {end_date}")
    print(f"统计天数：{row['days'] or 0} 天")
    print(f"总 Token 使用：{(row['total_tokens'] or 0):,}")
    print(f"总 Credits: {(row['credits'] or 0):,}")

    # 按工具汇总
    cursor.execute('''
        SELECT tool_name, SUM(total_tokens) as total_tokens, SUM(credits) as credits
        FROM daily_usage
        WHERE date BETWEEN ? AND ?
        GROUP BY tool_name
        ORDER BY total_tokens DESC
    ''', (start_date, end_date))

    print("\n📈 各工具使用量:")
    print("-" * 50)
    for row in cursor.fetchall():
        tokens_m = row['total_tokens'] / 1_000_000 if row['total_tokens'] else 0
        print(f"  {row['tool_name']}: {tokens_m:.2f}M tokens ({row['credits'] or 0} credits)")

    conn.close()
    print()


def cmd_today(args):
    """显示今日统计"""
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tool_name, model_name, total_tokens, credits
        FROM daily_usage
        WHERE date = ?
        ORDER BY tool_name
    ''', (today,))

    rows = cursor.fetchall()
    conn.close()

    print(f"\n📊 今日统计 ({today})")
    print("=" * 50)

    if not rows:
        print("  今日暂无数据")
        print("\n运行 'aistats collect' 采集数据")
    else:
        for row in rows:
            print(f"  {row['tool_name']}")
            if row['model_name']:
                print(f"    └─ {row['model_name']}: {row['total_tokens']:,} tokens")
            else:
                print(f"    └─ {row['total_tokens']:,} tokens ({row['credits'] or 0} credits)")
    print()


def cmd_tools(args):
    """列出所有工具"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tool_name, COUNT(DISTINCT date) as days, MAX(date) as last_used
        FROM daily_usage
        GROUP BY tool_name
        ORDER BY tool_name
    ''')

    print("\n🛠️  已记录的工具:")
    print("-" * 50)
    for row in cursor.fetchall():
        print(f"  {row['tool_name']}: {row['days']} 天 (最后：{row['last_used']})")

    conn.close()
    print()


def cmd_models(args):
    """列出所有模型"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT model_name, SUM(total_tokens) as total_tokens
        FROM daily_usage
        WHERE model_name IS NOT NULL
        GROUP BY model_name
        ORDER BY total_tokens DESC
    ''')

    print("\n🤖 已记录的模型:")
    print("-" * 50)
    for row in cursor.fetchall():
        tokens_m = row['total_tokens'] / 1_000_000 if row['total_tokens'] else 0
        print(f"  {row['model_name']}: {tokens_m:.2f}M tokens")

    conn.close()
    print()


def cmd_export(args):
    """导出数据为 JSON"""
    start_date, end_date = get_date_range(args.period)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, tool_name, model_name, total_tokens, credits
        FROM daily_usage
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
    ''', (start_date, end_date))

    rows = cursor.fetchall()
    conn.close()

    import json
    data = [dict(row) for row in rows]
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='AI 使用量统计 CLI')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # summary 命令
    p_summary = subparsers.add_parser('summary', help='显示汇总统计')
    p_summary.add_argument('--period', default='monthly',
                          choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly', 'all'],
                          help='时间范围')
    p_summary.set_defaults(func=cmd_summary)

    # today 命令
    p_today = subparsers.add_parser('today', help='显示今日统计')
    p_today.set_defaults(func=cmd_today)

    # tools 命令
    p_tools = subparsers.add_parser('tools', help='列出所有工具')
    p_tools.set_defaults(func=cmd_tools)

    # models 命令
    p_models = subparsers.add_parser('models', help='列出所有模型')
    p_models.set_defaults(func=cmd_models)

    # export 命令
    p_export = subparsers.add_parser('export', help='导出数据')
    p_export.add_argument('--period', default='monthly',
                         choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly', 'all'],
                         help='时间范围')
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
