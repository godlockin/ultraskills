#!/usr/bin/env python3
"""
夸克网盘下载 - 直接使用系统 Chrome 的 cookie
无需启动新浏览器，直接读取已登录的 Chrome cookie

用法:
  python use_chrome_cookies.py <分享链接> <保存目录> [提取码]

示例:
  python use_chrome_cookies.py \\
    "https://pan.quark.cn/s/ce476b55ec2a" \\
    "~/Documents/videos/沈弈斐" \\
    "7efe3YeNNj"

依赖:
  pip install browser-cookie3
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    import browser_cookie3
except ImportError:
    print("[错误] 缺少依赖: browser-cookie3")
    print("[安装] pip install browser-cookie3")
    sys.exit(1)

CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_DIR.mkdir(exist_ok=True)

def extract_chrome_cookies(domain='quark.cn'):
    """
    从系统 Chrome 中提取 cookie
    """
    print(f"[Cookie] 正在从 Chrome 读取 {domain} 的 cookie...")

    try:
        # 读取 Chrome cookies
        cookies = browser_cookie3.chrome(domain_name=domain)
        cookie_list = list(cookies)

        if not cookie_list:
            print(f"[警告] 未找到 {domain} 的 cookie")
            print("[提示] 请先在 Chrome 中登录夸克网盘")
            return None

        print(f"[成功] 找到 {len(cookie_list)} 个 cookie")

        # 转换为 Playwright 格式
        playwright_cookies = []
        for c in cookie_list:
            playwright_cookies.append({
                'name': c.name,
                'value': c.value,
                'domain': c.domain,
                'path': c.path,
                'expires': c.expires,
                'httpOnly': getattr(c, 'has_nonstandard_attr', lambda x: False)('HttpOnly'),
                'secure': c.secure
            })

        # 保存 Playwright 格式
        cookie_file = CONFIG_DIR / 'cookies.txt'
        with open(cookie_file, 'w') as f:
            f.write(str(playwright_cookies))

        # 保存字符串格式（用于 curl/wget）
        cookie_str = '; '.join([f"{c.name}={c.value}" for c in cookie_list])
        cookie_str_file = CONFIG_DIR / 'cookies_str.txt'
        with open(cookie_str_file, 'w') as f:
            f.write(cookie_str)

        print(f"[保存] cookies.txt (Playwright 格式)")
        print(f"[保存] cookies_str.txt (字符串格式)")

        return playwright_cookies

    except Exception as e:
        print(f"[错误] 读取 cookie 失败: {e}")
        print()
        print("[排查]:")
        print("  1. 确认已在 Chrome 中登录夸克网盘")
        print("  2. macOS 可能需要授权（系统偏好设置 → 隐私）")
        print("  3. 或运行 auto_download_cdp.py 自动登录")
        return None

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    os.makedirs(save_dir, exist_ok=True)

    print("=" * 80)
    print("夸克网盘下载 - 使用系统 Chrome Cookie")
    print("=" * 80)
    print()

    # 提取 Chrome cookies
    cookies = extract_chrome_cookies('quark.cn')

    if not cookies:
        print()
        print("[失败] 无法获取 cookie")
        print("[解决] 请先在 Chrome 中访问 https://pan.quark.cn 并登录")
        sys.exit(1)

    # 构造完整 URL
    full_url = f"{share_url}?pwd={password}" if password else share_url

    print()
    print("=" * 80)
    print("[Cookie 已提取] 现在可以使用 quark.py 下载")
    print("=" * 80)
    print()
    print("方式 1: 使用交互式工具（推荐）")
    print("  cd scripts && python quark.py")
    print("  选择: 1 (批量转存) 或 3 (批量下载)")
    print()
    print("方式 2: 在浏览器中手动操作")
    print(f"  已为你打开分享页面: {full_url}")
    print("  点击'保存到网盘'后，从网盘下载")
    print()

    # 在默认浏览器中打开分享链接
    subprocess.run(['open', full_url], check=False)

    print(f"[提示] 目标保存目录: {save_dir}")
    print(f"[提示] Cookie 有效期通常 30 天")

if __name__ == '__main__':
    main()
