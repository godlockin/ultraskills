#!/usr/bin/env python3
"""
夸克网盘下载 - 使用真实 Chrome 浏览器（CDP 连接）
绕过反自动化检测

用法:
  # 1. 先启动 Chrome with CDP
  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_quark &

  # 2. 运行此脚本
  python real_chrome_cdp.py <分享链接> <保存目录> [提取码]
"""

import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_DIR.mkdir(exist_ok=True)

def wait_for_login_real_chrome(page, timeout=300):
    """
    监控真实浏览器的登录状态
    """
    print("[等待] 请在浏览器中登录夸克网盘...")
    print("[提示] 推荐使用扫码登录（最快）")
    print()

    start_time = time.time()

    while time.time() - start_time < timeout:
        url = page.url

        # 检测登录成功
        if '/drive/' in url or '/home' in url or 'ucp.quark.cn' in url:
            print("[✓] 登录成功！")
            return True

        # 每 5 秒提示
        elapsed = int(time.time() - start_time)
        if elapsed > 0 and elapsed % 5 == 0:
            print(f"[等待中] {elapsed}s - 当前页面: {url[:60]}...")

        time.sleep(1)

    return False

def save_cookies(page):
    """保存 cookie"""
    cookies = page.context.cookies()

    # Playwright 格式
    cookie_file = CONFIG_DIR / 'cookies.txt'
    with open(cookie_file, 'w') as f:
        f.write(str(cookies))

    # 字符串格式（用于其他工具）
    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
    cookie_str_file = CONFIG_DIR / 'cookies_str.txt'
    with open(cookie_str_file, 'w') as f:
        f.write(cookie_str)

    print(f"[Cookie] 已保存 {len(cookies)} 个键值对")
    return cookies

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    os.makedirs(save_dir, exist_ok=True)

    print("=" * 80)
    print("夸克网盘下载工具 - Real Chrome CDP 模式")
    print("=" * 80)
    print(f"链接: {share_url}")
    print(f"密码: {password or '无'}")
    print(f"目标: {save_dir}")
    print()

    with sync_playwright() as p:
        try:
            # 连接到已运行的 Chrome（CDP 端口 9222）
            print("[连接] 正在连接 Chrome (CDP 端口 9222)...")
            browser = p.chromium.connect_over_cdp('http://localhost:9222')

            # 获取当前页面（或创建新页面）
            if browser.contexts and browser.contexts[0].pages:
                page = browser.contexts[0].pages[0]
                print("[连接] 使用已有标签页")
            else:
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.new_page()
                print("[连接] 创建新标签页")

        except Exception as e:
            print(f"[错误] 无法连接 Chrome CDP: {e}")
            print()
            print("请先启动 Chrome with CDP:")
            print("  macOS:")
            print('    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_quark &')
            print()
            print("  Linux:")
            print('    google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_quark &')
            print()
            print("  Windows:")
            print('    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\\temp\\chrome_quark')
            sys.exit(1)

        # 打开夸克网盘
        print("[访问] 正在打开夸克网盘...")
        page.goto('https://pan.quark.cn')
        time.sleep(2)

        # 检查是否已登录
        if '/drive/' in page.url or '/home' in page.url:
            print("[登录] 已登录状态")
        else:
            # 等待登录
            if not wait_for_login_real_chrome(page, timeout=300):
                print("[失败] 登录超时")
                sys.exit(1)

        # 保存 cookie
        cookies = save_cookies(page)

        # 访问分享链接
        print()
        print(f"[访问] 正在打开分享链接...")
        full_url = f"{share_url}?pwd={password}" if password else share_url
        page.goto(full_url)
        time.sleep(3)

        print()
        print("=" * 80)
        print("[下一步] 请在浏览器中完成以下操作:")
        print("  1. 点击'保存到网盘'按钮（推荐）")
        print("  2. 或点击'下载'按钮")
        print()
        print("  转存后可以随时从网盘下载，分享链接失效也不影响")
        print("=" * 80)
        print()
        print("[等待] 浏览器保持打开，完成操作后按 Enter 关闭...")

        # 保持浏览器打开，等待用户操作
        input()

        print("[完成] Cookie 已保存，下次可直接使用")
        print(f"[完成] 保存位置: {CONFIG_DIR / 'cookies.txt'}")

if __name__ == '__main__':
    main()
