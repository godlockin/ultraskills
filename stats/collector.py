#!/usr/bin/env python3
"""
AI 使用量数据采集脚本
采集各 AI 工具的 token/credit 使用量并存储到 SQLite 数据库
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 数据库路径
DB_PATH = Path(__file__).parent / "ai_usage.db"

# 各工具的数据文件路径
CLAUDE_STATS_FILE = Path.home() / ".claude" / "stats-cache.json"
MANUAL_USAGE_FILE = Path.home() / ".claude" / "ai-stats" / "manual_usage.json"


def init_database():
    """初始化 SQLite 数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建每日使用量表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            model_name TEXT,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            total_tokens INTEGER DEFAULT 0,
            credits INTEGER DEFAULT 0,
            cost_usd REAL DEFAULT 0,
            message_count INTEGER DEFAULT 0,
            tool_call_count INTEGER DEFAULT 0,
            session_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, tool_name, model_name)
        )
    ''')

    # 创建索引
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_date ON daily_usage(date)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_tool ON daily_usage(tool_name)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_date_tool ON daily_usage(date, tool_name)
    ''')

    conn.commit()
    conn.close()
    logger.info(f"数据库初始化完成：{DB_PATH}")


def get_claude_code_stats() -> List[Dict[str, Any]]:
    """获取 Claude Code 的使用统计"""
    stats = []
    today = datetime.now().strftime("%Y-%m-%d")

    if not CLAUDE_STATS_FILE.exists():
        logger.warning(f"Claude Code 统计文件不存在：{CLAUDE_STATS_FILE}")
        return stats

    try:
        with open(CLAUDE_STATS_FILE, 'r') as f:
            data = json.load(f)

        # 获取每日活动数据
        daily_activity = data.get('dailyActivity', [])
        today_activity = next(
            (item for item in daily_activity if item.get('date') == today),
            None
        )

        if today_activity:
            stats.append({
                'date': today,
                'tool_name': 'Claude Code',
                'model_name': None,
                'input_tokens': 0,
                'output_tokens': 0,
                'total_tokens': 0,
                'message_count': today_activity.get('messageCount', 0),
                'tool_call_count': today_activity.get('toolCallCount', 0),
                'session_count': today_activity.get('sessionCount', 0),
            })

        # 获取各模型的 token 使用
        model_usage = data.get('modelUsage', {})
        for model_name, usage in model_usage.items():
            input_tokens = usage.get('inputTokens', 0)
            output_tokens = usage.get('outputTokens', 0)
            stats.append({
                'date': today,
                'tool_name': 'Claude Code',
                'model_name': model_name,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens,
            })

    except Exception as e:
        logger.error(f"读取 Claude Code 统计失败：{e}")

    return stats


def get_manual_stats() -> List[Dict[str, Any]]:
    """获取手动记录的使用统计"""
    stats = []
    today = datetime.now().strftime("%Y-%m-%d")

    if not MANUAL_USAGE_FILE.exists():
        return stats

    try:
        with open(MANUAL_USAGE_FILE, 'r') as f:
            data = json.load(f)

        daily_records = data.get('daily', [])
        today_record = next(
            (item for item in daily_records if item.get('date') == today),
            None
        )

        if today_record:
            for tool in today_record.get('tools', []):
                stats.append({
                    'date': today,
                    'tool_name': tool.get('name', 'Unknown'),
                    'model_name': None,
                    'credits': tool.get('credits', 0),
                })

    except Exception as e:
        logger.error(f"读取手动记录失败：{e}")

    return stats


def get_cursor_stats() -> List[Dict[str, Any]]:
    """获取 Cursor 的使用统计（需要手动记录或 API）"""
    # Cursor 没有公开的本地 API，需要手动记录
    # 可以从 ~/.cursor/config 或环境变量读取
    logger.debug("Cursor 统计需要手动记录")
    return []


def get_trae_stats() -> List[Dict[str, Any]]:
    """获取 Trae 的使用统计"""
    # Trae 的本地统计文件位置
    trae_config_dir = Path.home() / "Library" / "Application Support" / "Trae"
    logger.debug(f"Trae 配置目录：{trae_config_dir}")
    return []


def collect_all_stats() -> List[Dict[str, Any]]:
    """收集所有工具的统计信息"""
    all_stats = []

    # 自动采集
    all_stats.extend(get_claude_code_stats())
    all_stats.extend(get_manual_stats())

    # 需要手动记录的工具
    all_stats.extend(get_cursor_stats())
    all_stats.extend(get_trae_stats())

    return all_stats


def save_to_database(stats: List[Dict[str, Any]]):
    """保存统计数据到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for stat in stats:
        cursor.execute('''
            INSERT OR REPLACE INTO daily_usage
            (date, tool_name, model_name, input_tokens, output_tokens, total_tokens,
             credits, message_count, tool_call_count, session_count, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            stat.get('date'),
            stat.get('tool_name'),
            stat.get('model_name'),
            stat.get('input_tokens', 0),
            stat.get('output_tokens', 0),
            stat.get('total_tokens', 0),
            stat.get('credits', 0),
            stat.get('message_count', 0),
            stat.get('tool_call_count', 0),
            stat.get('session_count', 0),
        ))

    conn.commit()
    conn.close()
    logger.info(f"已保存 {len(stats)} 条统计数据到数据库")


def add_manual_record(tool_name: str, credits: int, date: str = None):
    """添加手动记录（如果已存在则更新）"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 先检查是否已存在该日期和工具的记录
    cursor.execute('''
        SELECT id FROM daily_usage
        WHERE date = ? AND tool_name = ? AND model_name IS NULL
    ''', (date, tool_name))

    existing = cursor.fetchone()

    if existing:
        # 更新现有记录
        cursor.execute('''
            UPDATE daily_usage
            SET credits = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (credits, existing[0]))
        logger.info(f"已更新手动记录：{tool_name} = {credits} credits ({date})")
    else:
        # 插入新记录
        stat = {
            'date': date,
            'tool_name': tool_name,
            'model_name': None,
            'credits': credits,
        }
        save_to_database([stat])
        logger.info(f"已添加手动记录：{tool_name} = {credits} credits ({date})")

    conn.commit()
    conn.close()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="AI 使用量数据采集")
    parser.add_argument('action', choices=['collect', 'init', 'add'],
                       default='collect', help='操作类型')
    parser.add_argument('--tool', type=str, help='工具名称（用于 add 操作）')
    parser.add_argument('--credits', type=int, help='Credit 数量（用于 add 操作）')
    parser.add_argument('--date', type=str, help='日期（YYYY-MM-DD，用于 add 操作）')

    args = parser.parse_args()

    if args.action == 'init':
        init_database()
    elif args.action == 'collect':
        init_database()
        stats = collect_all_stats()
        save_to_database(stats)
        print(f"✅ 已采集 {len(stats)} 条统计数据")
    elif args.action == 'add':
        if not args.tool or args.credits is None:
            print("用法：python collector.py add --tool <工具名> --credits <数量> [--date <日期>]")
            return
        init_database()
        add_manual_record(args.tool, args.credits, args.date)


if __name__ == "__main__":
    main()
