#!/usr/bin/env python3
"""CodeGraph健康检查脚本"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def check_codegraph_installed():
    """检查CodeGraph是否安装"""
    try:
        result = subprocess.run(
            ['codegraph', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✓ CodeGraph installed: {version}")
            return True
        else:
            print("❌ CodeGraph not installed")
            print("   Install: curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh")
            return False
    except FileNotFoundError:
        print("❌ CodeGraph not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking CodeGraph: {e}")
        return False

def check_index_exists(project_root="."):
    """检查索引是否存在"""
    index_path = Path(project_root) / ".codegraph" / "codegraph.db"
    if index_path.exists():
        size_mb = index_path.stat().st_size / 1024 / 1024
        print(f"✓ Index exists: .codegraph/codegraph.db ({size_mb:.1f}MB)")
        
        # 检查修改时间
        mtime = datetime.fromtimestamp(index_path.stat().st_mtime)
        age = datetime.now() - mtime
        if age.total_seconds() < 300:  # 5分钟内
            print(f"✓ Index fresh: last updated {int(age.total_seconds())} seconds ago")
        elif age.total_seconds() < 3600:  # 1小时内
            print(f"⚠️  Index aging: last updated {int(age.total_seconds() / 60)} minutes ago")
        else:
            print(f"⚠️  Index stale: last updated {int(age.total_seconds() / 3600)} hours ago")
            print("   Consider: codegraph sync")
        
        return True
    else:
        print("❌ Index not found")
        print("   Initialize: codegraph init -i")
        return False

def check_index_stats(project_root="."):
    """获取索引统计信息"""
    try:
        result = subprocess.run(
            ['codegraph', 'status', project_root],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            # 解析输出
            stats = {}
            for line in result.stdout.split('\n'):
                if 'symbols' in line.lower():
                    stats['symbols'] = line.strip()
                elif 'edges' in line.lower():
                    stats['edges'] = line.strip()
                elif 'languages' in line.lower():
                    stats['languages'] = line.strip()
            
            if stats:
                print(f"✓ Stats: {stats.get('symbols', 'N/A')} | {stats.get('edges', 'N/A')} | {stats.get('languages', 'N/A')}")
            else:
                # 直接显示原始输出
                relevant_lines = [l for l in result.stdout.split('\n') if l.strip() and not l.startswith('─')]
                for line in relevant_lines[:5]:
                    print(f"  {line}")
            return True
        else:
            print("⚠️  Cannot read stats")
            return False
    except Exception as e:
        print(f"⚠️  Error reading stats: {e}")
        return False

def check_watcher_status():
    """检查文件监听是否启用"""
    # CodeGraph的watcher是MCP server启动时自动运行的
    # 这里只能间接检查
    print("ℹ️  Watcher: auto-enabled when MCP server runs")
    print("   Verify: check ~/.claude.json for codegraph server config")

def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("=" * 70)
    print("CodeGraph 健康检查")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 检查安装
    if not check_codegraph_installed():
        all_ok = False
    
    print()
    
    # 检查索引
    if not check_index_exists(project_root):
        all_ok = False
        print()
        print("=" * 70)
        print("❌ CodeGraph 未就绪")
        print("=" * 70)
        sys.exit(1)
    
    print()
    
    # 检查统计
    check_index_stats(project_root)
    
    print()
    
    # 检查监听器
    check_watcher_status()
    
    print()
    print("=" * 70)
    if all_ok:
        print("✅ CodeGraph 运行正常")
    else:
        print("⚠️  存在部分问题")
    print("=" * 70)

if __name__ == '__main__':
    main()
