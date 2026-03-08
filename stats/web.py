#!/usr/bin/env python3
"""
AI 使用量统计 Web 界面
使用 Flask 提供 REST API 和前端页面
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
from flask import Flask, jsonify, request, send_from_directory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')

DB_PATH = Path(__file__).parent / "ai_usage.db"


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_date_range(period: str) -> tuple:
    """根据时间范围获取起止日期"""
    today = datetime.now().date()

    if period == 'daily':
        start = today
        end = today
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
        start = today
        end = today

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


@app.route('/')
def index():
    """首页"""
    return send_from_directory('static', 'index.html')


@app.route('/api/stats')
def get_stats():
    """获取统计数据"""
    period = request.args.get('period', 'monthly')
    tool = request.args.get('tool', None)

    start_date, end_date = get_date_range(period)

    conn = get_db_connection()
    cursor = conn.cursor()

    if tool:
        cursor.execute('''
            SELECT date, tool_name, model_name,
                   SUM(input_tokens) as input_tokens,
                   SUM(output_tokens) as output_tokens,
                   SUM(total_tokens) as total_tokens,
                   SUM(credits) as credits,
                   SUM(message_count) as message_count,
                   SUM(tool_call_count) as tool_call_count,
                   SUM(session_count) as session_count
            FROM daily_usage
            WHERE date BETWEEN ? AND ?
              AND tool_name = ?
            GROUP BY date, tool_name, model_name
            ORDER BY date DESC
        ''', (start_date, end_date, tool))
    else:
        cursor.execute('''
            SELECT date, tool_name, model_name,
                   SUM(input_tokens) as input_tokens,
                   SUM(output_tokens) as output_tokens,
                   SUM(total_tokens) as total_tokens,
                   SUM(credits) as credits,
                   SUM(message_count) as message_count,
                   SUM(tool_call_count) as tool_call_count,
                   SUM(session_count) as session_count
            FROM daily_usage
            WHERE date BETWEEN ? AND ?
            GROUP BY date, tool_name, model_name
            ORDER BY date DESC, tool_name
        ''', (start_date, end_date))

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            'date': row['date'],
            'tool_name': row['tool_name'],
            'model_name': row['model_name'],
            'input_tokens': row['input_tokens'] or 0,
            'output_tokens': row['output_tokens'] or 0,
            'total_tokens': row['total_tokens'] or 0,
            'credits': row['credits'] or 0,
            'message_count': row['message_count'] or 0,
            'tool_call_count': row['tool_call_count'] or 0,
            'session_count': row['session_count'] or 0,
        })

    return jsonify(result)


@app.route('/api/tools')
def get_tools():
    """获取所有工具列表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT tool_name FROM daily_usage ORDER BY tool_name')
    rows = cursor.fetchall()
    conn.close()

    tools = [row['tool_name'] for row in rows]
    return jsonify(tools)


@app.route('/api/summary')
def get_summary():
    """获取汇总统计"""
    period = request.args.get('period', 'monthly')
    start_date, end_date = get_date_range(period)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 按工具汇总
    cursor.execute('''
        SELECT tool_name,
               SUM(total_tokens) as total_tokens,
               SUM(credits) as credits,
               COUNT(DISTINCT date) as days
        FROM daily_usage
        WHERE date BETWEEN ? AND ?
        GROUP BY tool_name
        ORDER BY total_tokens DESC
    ''', (start_date, end_date))

    tool_summary = []
    for row in cursor.fetchall():
        tool_summary.append({
            'tool_name': row['tool_name'],
            'total_tokens': row['total_tokens'] or 0,
            'credits': row['credits'] or 0,
            'days': row['days'] or 0,
        })

    # 总体汇总
    cursor.execute('''
        SELECT SUM(total_tokens) as total_tokens,
               SUM(credits) as credits,
               COUNT(DISTINCT date) as days
        FROM daily_usage
        WHERE date BETWEEN ? AND ?
    ''', (start_date, end_date))

    row = cursor.fetchone()
    overall = {
        'total_tokens': row['total_tokens'] or 0,
        'credits': row['credits'] or 0,
        'days': row['days'] or 0,
    }

    conn.close()

    return jsonify({
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'overall': overall,
        'by_tool': tool_summary,
    })


@app.route('/api/models')
def get_models():
    """获取所有模型列表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT model_name FROM daily_usage WHERE model_name IS NOT NULL ORDER BY model_name')
    rows = cursor.fetchall()
    conn.close()

    models = [row['model_name'] for row in rows if row['model_name']]
    return jsonify(models)


def create_static_dir():
    """创建静态文件目录"""
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    logger.info(f"静态文件目录已创建：{static_dir}")


if __name__ == "__main__":
    create_static_dir()
    app.run(host="0.0.0.0", port=5000, debug=True)
