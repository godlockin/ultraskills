#!/usr/bin/env python3
"""
generate.py - 自动生成新的 Skill

基于用户任务描述和 _template_skill 模板生成新的 SKILL.md。
"""

import os
import sys
import json
import datetime
import re


def sanitize_name(name: str) -> str:
    """将名称转换为安全的 kebab-case 格式"""
    # 移除非单词字符（保留 Unicode 字符如中文、连字符）
    safe = re.sub(r'[^\w\s-]', '', name, flags=re.UNICODE)
    # 替换空格为连字符
    safe = re.sub(r'\s+', '-', safe)
    # 转小写
    return safe.lower()


def load_template(template_path: str = "_template_skill/SKILL.md") -> str:
    """加载 Skill 模板"""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_skill_description(task: str) -> str:
    """基于任务描述生成 Skill 描述"""
    return f"用于 {task} 的 Skill"


def extract_goals(task: str) -> list:
    """从任务描述中提取目标"""
    # 简单实现：基于任务关键词生成目标
    goals = [
        f"实现 {task} 功能",
        "提供清晰的工作流程",
        "包含最佳实践"
    ]
    return goals


def extract_tags(task: str) -> list:
    """从任务描述中提取标签"""
    # 简单的关键词到标签的映射
    keyword_tags = {
        "视频": ["video", "media"],
        "图片": ["image", "media"],
        "音频": ["audio", "media"],
        "文档": ["document", "productivity"],
        "代码": ["code", "engineering"],
        "Git": ["git", "version-control"],
        "测试": ["testing", "quality"],
        "部署": ["deployment", "devops"],
    }

    tags = ["auto-generated"]
    task_lower = task.lower()

    for keyword, tag_list in keyword_tags.items():
        if keyword in task_lower:
            tags.extend(tag_list)

    return list(set(tags))[:5]  # 最多5个标签


def generate_skill(task: str, output_dir: str = ".") -> str:
    """
    根据任务描述生成新的 Skill

    Args:
        task: 用户任务描述
        output_dir: 输出目录

    Returns:
        创建的 Skill 路径
    """
    # 生成安全的目录名
    skill_name = sanitize_name(task)
    skill_path = os.path.join(output_dir, skill_name)

    # 创建目录结构
    scripts_dir = os.path.join(skill_path, "scripts")
    examples_dir = os.path.join(skill_path, "examples")
    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(examples_dir, exist_ok=True)

    # 生成 SKILL.md
    template = load_template()
    goals = extract_goals(task)
    tags = extract_tags(task)

    skill_md = f"""---
name: {skill_name}
description: {generate_skill_description(task)}
version: 0.1.0
tags: [{', '.join(tags)}]
created_at: {datetime.datetime.now().isoformat()}
auto_generated: true
---

# {task}

> 用于 {task} 的 Skill（自动生成）

## 🎯 目标

{chr(10).join(f'* {goal}' for goal in goals)}

## 🧠 核心理念

[TODO: 描述这个 Skill 背后的方法论]

## 🚀 使用流程

### Step 1: 准备 (Preparation)

[TODO: 要做什么准备工作]

### Step 2: 执行 (Execution)

[核心步骤]

### Step 3: 验证 (Verification)

[如何检查结果]

## 💡 最佳实践

* **Do**: 应该做的
* **Don't**: 不应该做的

## 📚 资源引用

* [示例](./examples/basic-usage.md)
* [脚本](./scripts/main.py)
"""

    skill_md_path = os.path.join(skill_path, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    # 创建入口脚本占位
    main_py = f'''#!/usr/bin/env python3
"""
main.py - {task} 入口脚本

[TODO: 实现具体逻辑]
"""

import sys


def main():
    """主入口函数"""
    print("This is a placeholder for {task}.")
    print("TODO: Implement actual logic here.")


if __name__ == "__main__":
    main()
'''

    with open(os.path.join(scripts_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py)

    # 创建使用示例占位
    usage_md = f"""# {task} 基础用法

## 场景

[TODO: 描述使用场景]

## 输入

```
[TODO: 输入示例]
```

## 执行

```bash
python scripts/main.py [args]
```

## 输出

```
[TODO: 输出示例]
```
"""

    with open(os.path.join(examples_dir, "basic-usage.md"), "w", encoding="utf-8") as f:
        f.write(usage_md)

    return skill_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate.py <task_description> [output_dir]")
        print("Example: python generate.py 视频剪辑 ./my-skills")
        sys.exit(1)

    task = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    skill_path = generate_skill(task, output_dir)

    print(f"✅ Skill 已生成: {skill_path}")
    print("\n📋 下一步:")
    print("1. 查看并完善 SKILL.md")
    print("2. 实现 scripts/main.py 中的实际逻辑")
    print("3. 完善 examples/basic-usage.md 示例")


if __name__ == "__main__":
    main()