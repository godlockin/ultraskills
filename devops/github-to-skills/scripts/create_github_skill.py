#!/usr/bin/env python3
"""
create_github_skill.py - 创建 GitHub Skill 脚手架

根据仓库信息创建标准化的 Skill 目录结构。
"""

import sys
import os
import json
import datetime


def create_skill(repo_info: dict, output_dir: str) -> str:
    """
    根据 GitHub 仓库信息创建 Skill 脚手架。
    
    Args:
        repo_info: 包含 name, url, latest_hash, readme 的字典
        output_dir: 输出目录
        
    Returns:
        创建的 Skill 路径
    """
    repo_name = repo_info['name']
    # 转换为安全的目录名 (kebab-case)
    safe_name = "".join(
        c if c.isalnum() or c in ('-', '_') else '-' 
        for c in repo_name
    ).lower()
    
    skill_path = os.path.join(output_dir, safe_name)
    
    # 1. 创建目录结构
    os.makedirs(os.path.join(skill_path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "examples"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "references"), exist_ok=True)
    
    # 2. 生成 SKILL.md (带扩展元数据)
    readme_excerpt = repo_info.get('readme', '')[:500]
    if len(repo_info.get('readme', '')) > 500:
        readme_excerpt += "..."
        
    skill_md_content = f"""---
name: {safe_name}
description: Skill wrapper for {repo_info['name']}. 自动生成自 {repo_info['url']}。
version: 0.1.0
tags: [github-wrapped, auto-generated]
# 扩展元数据 (用于 skill-manager)
github_url: {repo_info['url']}
github_hash: {repo_info['latest_hash']}
created_at: {datetime.datetime.now().isoformat()}
entry_point: scripts/wrapper.py
---

# {repo_info['name']} Skill

> 此 Skill 封装了 [{repo_info['name']}]({repo_info['url']}) 的功能。

## 🎯 目标

[TODO: 描述此工具解决的问题]

## 📖 概述

{readme_excerpt}

## 🚀 使用方式

### 前置条件

确保已安装以下依赖：
- [TODO: 根据 requirements.txt 列出依赖]

### 基本用法

```bash
# [TODO: 添加具体调用示例]
```

## 📚 资源

- [原始仓库]({repo_info['url']})
- [wrapper.py](./scripts/wrapper.py) - 调用入口
"""
    
    with open(os.path.join(skill_path, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md_content)
        
    # 3. 创建占位 Wrapper 脚本
    wrapper_content = f'''#!/usr/bin/env python3
"""
wrapper.py - {repo_name} 调用封装

此脚本封装了 {repo_name} 的调用逻辑。
"""

import sys
import subprocess


def main():
    """主入口函数。"""
    print("This is a placeholder wrapper for {repo_name}.")
    print("TODO: Implement actual invocation logic.")
    
    # 示例调用模式:
    # subprocess.run(['{repo_name}', *sys.argv[1:]], check=True)


if __name__ == "__main__":
    main()
'''
    
    with open(os.path.join(skill_path, "scripts", "wrapper.py"), "w", encoding="utf-8") as f:
        f.write(wrapper_content)
        
    # 4. 创建基础示例
    example_content = f"""# {repo_info['name']} 基础用法

## 场景

[TODO: 描述使用场景]

## 输入

```
[TODO: 输入示例]
```

## 执行

```bash
python scripts/wrapper.py [args]
```

## 输出

```
[TODO: 输出示例]
```
"""
    
    with open(os.path.join(skill_path, "examples", "basic-usage.md"), "w", encoding="utf-8") as f:
        f.write(example_content)

    return skill_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python create_github_skill.py <json_info_file> <output_skills_dir>")
        print("\nExample:")
        print("  python create_github_skill.py /tmp/repo_info.json ~/.claude/skills/")
        sys.exit(1)
        
    json_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    with open(json_file, 'r', encoding='utf-8') as f:
        repo_info = json.load(f)
        
    skill_path = create_skill(repo_info, output_dir)
    
    print(f"✅ Skill scaffolded at: {skill_path}")
    print("\n📋 Next steps:")
    print("1. Review SKILL.md and refine the description")
    print("2. Implement the actual logic in scripts/wrapper.py")
    print("3. Add real examples to examples/")


if __name__ == "__main__":
    main()
