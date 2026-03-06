#!/usr/bin/env python3
"""
merge_evolution.py - 增量合并经验数据

将新的经验数据合并到 evolution.json 中，自动去重。
"""

import os
import sys
import json
import datetime
from typing import Dict, List


def merge_evolution(skill_dir: str, new_data_json_str: str) -> bool:
    """
    增量合并经验数据。
    
    Args:
        skill_dir: skill 目录路径
        new_data_json_str: 新数据的 JSON 字符串
        
    Returns:
        是否成功
    """
    evolution_json_path = os.path.join(skill_dir, "evolution.json")
    
    # 1. 加载现有数据或创建新的
    current_data: Dict = {}
    if os.path.exists(evolution_json_path):
        try:
            with open(evolution_json_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Warning: Could not parse existing evolution.json: {e}", file=sys.stderr)
            current_data = {}

    # 2. 解析新数据
    try:
        new_data = json.loads(new_data_json_str)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        return False

    # 3. 合并逻辑
    # 更新时间戳
    current_data['last_updated'] = datetime.datetime.now().isoformat()
    
    # 合并列表字段 (去重)
    for list_key in ['preferences', 'fixes', 'contexts']:
        if list_key in new_data:
            existing_list: List = current_data.get(list_key, [])
            new_items = new_data[list_key]
            if isinstance(new_items, list):
                for item in new_items:
                    if item not in existing_list:
                        existing_list.append(item)
                current_data[list_key] = existing_list
                
    # 覆盖 custom_prompts (假设 Agent 发送的是最终期望状态)
    if 'custom_prompts' in new_data:
        current_data['custom_prompts'] = new_data['custom_prompts']

    # 更新 hash 标记
    if 'last_evolved_hash' in new_data:
        current_data['last_evolved_hash'] = new_data['last_evolved_hash']

    # 4. 保存
    try:
        with open(evolution_json_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Successfully merged evolution data for {os.path.basename(skill_dir)}")
        return True
    except Exception as e:
        print(f"❌ Error saving evolution.json: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python merge_evolution.py <skill_dir> <json_string>")
        print("\nExample:")
        print('  python merge_evolution.py ~/.claude/skills/yt-dlp/ \'{"preferences": ["默认静音"]}\'')
        sys.exit(1)
        
    skill_dir = sys.argv[1]
    json_str = sys.argv[2]
    
    success = merge_evolution(skill_dir, json_str)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
