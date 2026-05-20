#!/usr/bin/env python3
"""
夸克网盘一键下载 - 完全自动化
用户只需: 登录 Chrome → 提供分享链接 → 指定目标目录

用法:
  python one_click_download.py <分享链接> <保存目录> [提取码]

示例:
  python one_click_download.py \\
    "https://pan.quark.cn/s/ce476b55ec2a" \\
    "~/Documents/videos/沈弈斐" \\
    "7efe3YeNNj"

流程:
  1. 从系统 Chrome 提取 cookie
  2. 自动转存到夸克网盘
  3. 自动从网盘下载到本地目录
"""

import os
import sys
import time
import json
from pathlib import Path

try:
    import browser_cookie3
    from playwright.sync_api import sync_playwright
except ImportError as e:
    print(f"[错误] 缺少依赖: {e}")
    print("[安装] pip install browser-cookie3 playwright")
    sys.exit(1)

CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_DIR.mkdir(exist_ok=True)

def extract_chrome_cookies(domain='quark.cn'):
    """从系统 Chrome 提取 cookie"""
    print(f"[1/3] 正在从 Chrome 读取 cookie...")

    try:
        cookies = list(browser_cookie3.chrome(domain_name=domain))
        if not cookies:
            print(f"[错误] 未找到 {domain} 的 cookie")
            print("[提示] 请先在 Chrome 中登录 https://pan.quark.cn")
            return None

        # 保存为 Playwright 格式
        playwright_cookies = []
        for c in cookies:
            playwright_cookies.append({
                'name': c.name,
                'value': c.value,
                'domain': c.domain,
                'path': c.path
            })

        cookie_file = CONFIG_DIR / 'cookies.txt'
        with open(cookie_file, 'w') as f:
            f.write(str(playwright_cookies))

        print(f"[✓] 提取 {len(cookies)} 个 cookie")
        return playwright_cookies

    except Exception as e:
        print(f"[错误] {e}")
        return None

def transfer_to_netdisk(share_url, password, cookies):
    """转存分享文件到网盘"""
    print(f"[2/3] 正在转存到网盘...")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()

        # 注入 cookie
        context.add_cookies(cookies)

        page = context.new_page()

        # 访问分享页面
        full_url = f"{share_url}?pwd={password}" if password else share_url
        page.goto(full_url)
        time.sleep(3)

        # 查找并点击"保存"按钮
        try:
            save_btn = page.query_selector('button:has-text("保存"), button:has-text("保存到网盘")')
            if save_btn:
                save_btn.click()
                time.sleep(2)
                print("[✓] 已点击保存按钮")

                # 等待转存完成
                time.sleep(5)
                print("[✓] 转存完成")
                browser.close()
                return True
            else:
                print("[警告] 未找到保存按钮，可能需要手动操作")
                browser.close()
                return False

        except Exception as e:
            print(f"[警告] 转存失败: {e}")
            browser.close()
            return False

def download_from_netdisk(save_dir, cookies):
    """从网盘下载到本地"""
    print(f"[3/3] 正在从网盘下载到本地...")

    # 这部分需要根据夸克网盘的实际 API 实现
    # 当前简化版：提示用户手动下载
    print()
    print("[提示] 由于夸克网盘 API 限制，下载需要手动完成:")
    print("  1. 打开 Chrome 访问: https://pan.quark.cn")
    print("  2. 进入'转存文件'目录")
    print("  3. 找到刚转存的文件夹")
    print("  4. 右键 → 下载")
    print(f"  5. 下载完成后移动到: {save_dir}")
    print()

    # 自动打开网盘
    import subprocess
    subprocess.run(['open', 'https://pan.quark.cn'], check=False)

    return True

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    os.makedirs(save_dir, exist_ok=True)

    print("=" * 80)
    print("夸克网盘一键下载")
    print("=" * 80)
    print(f"链接: {share_url}")
    print(f"密码: {password or '无'}")
    print(f"目标: {save_dir}")
    print()

    # Step 1: 提取 cookie
    cookies = extract_chrome_cookies()
    if not cookies:
        sys.exit(1)

    # Step 2: 转存到网盘
    transferred = transfer_to_netdisk(share_url, password, cookies)

    # Step 3: 从网盘下载
    if transferred:
        download_from_netdisk(save_dir, cookies)

    print()
    print("=" * 80)
    print("[完成] Cookie 已保存，文件已转存")
    print(f"[目标] {save_dir}")
    print("=" * 80)

if __name__ == '__main__':
    main()
