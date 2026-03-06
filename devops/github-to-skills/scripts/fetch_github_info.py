#!/usr/bin/env python3
"""
fetch_github_info.py - 获取 GitHub 仓库信息

从 GitHub 仓库获取元数据，包括名称、最新 commit hash 和 README 内容。
使用 git ls-remote 避免完整克隆。
"""

import sys
import json
import subprocess
import urllib.request
import urllib.error


def get_repo_info(url: str) -> dict:
    """
    获取仓库信息。
    
    Args:
        url: GitHub 仓库 URL
        
    Returns:
        包含 name, url, latest_hash, readme 的字典
    """
    # 规范化 URL
    clean_url = url.rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
        
    repo_name = clean_url.split('/')[-1]
    
    # 1. 获取最新 Commit Hash (使用 git ls-remote 避免完整克隆)
    latest_hash = "unknown"
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            latest_hash = result.stdout.split()[0]
    except subprocess.TimeoutExpired:
        print("Warning: git ls-remote timed out", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Failed to fetch git info: {e}", file=sys.stderr)

    # 2. 获取 README (尝试 main, 然后 master)
    readme_content = ""
    readme_url_base = clean_url.replace("github.com", "raw.githubusercontent.com")
    
    for branch in ["main", "master"]:
        for filename in ["README.md", "readme.md", "Readme.md"]:
            try:
                readme_url = f"{readme_url_base}/{branch}/{filename}"
                req = urllib.request.Request(
                    readme_url,
                    headers={'User-Agent': 'github-to-skills/1.0'}
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    readme_content = response.read().decode('utf-8')
                    break
            except (urllib.error.HTTPError, urllib.error.URLError):
                continue
        if readme_content:
            break

    # 3. 构建结果
    return {
        "name": repo_name,
        "url": clean_url,
        "latest_hash": latest_hash,
        "readme": readme_content[:10000]  # 截断以避免上下文过大
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_github_info.py <github_url>")
        print("\nExample:")
        print("  python fetch_github_info.py https://github.com/yt-dlp/yt-dlp")
        sys.exit(1)
        
    url = sys.argv[1]
    info = get_repo_info(url)
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
