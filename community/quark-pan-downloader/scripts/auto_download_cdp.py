#!/usr/bin/env python3
"""
夸克网盘自动下载脚本 - Chrome CDP 版本
功能：打开 Chrome → 等待登录 → 自动获取 cookie → 下载文件

使用方式:
  python auto_download_cdp.py <分享链接> <保存目录> [提取码]

示例:
  python auto_download_cdp.py "https://pan.quark.cn/s/ce476b55ec2a" "~/Downloads/沈弈斐" "7efe3YeNNj"
"""

import os
import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_DIR.mkdir(exist_ok=True)

def wait_for_login(page: Page, timeout: int = 300) -> bool:
    """
    等待用户登录成功

    通过检测页面 URL 或特定元素判断登录状态
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        current_url = page.url

        # 检查是否已登录（URL 包含 /drive/ 或存在用户信息元素）
        if '/drive/' in current_url or '/home' in current_url:
            print("[成功] 检测到登录成功！")
            return True

        # 检查是否有用户信息（通过 localStorage）
        try:
            user_info = page.evaluate("() => localStorage.getItem('userInfo')")
            if user_info:
                print("[成功] 检测到用户信息！")
                return True
        except:
            pass

        time.sleep(1)

        # 每 10 秒提示一次
        elapsed = int(time.time() - start_time)
        if elapsed > 0 and elapsed % 10 == 0:
            print(f"[等待中] 已等待 {elapsed} 秒...")

    print(f"[超时] 等待登录超过 {timeout} 秒")
    return False

def save_cookies_playwright_format(page: Page) -> str:
    """
    获取并保存 cookie（Playwright 格式）
    """
    cookies = page.context.cookies()

    cookie_file = CONFIG_DIR / 'cookies.txt'
    with open(cookie_file, 'w') as f:
        f.write(str(cookies))

    print(f"[Cookie] 已保存到: {cookie_file}")
    print(f"[Cookie] 共 {len(cookies)} 个键值对")

    # 同时保存为字符串格式（调试用）
    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
    cookie_str_file = CONFIG_DIR / 'cookies_str.txt'
    with open(cookie_str_file, 'w') as f:
        f.write(cookie_str)

    return str(cookies)

def download_from_share(page: Page, share_url: str, password: str = None, save_dir: str = './downloads'):
    """
    从分享链接下载文件
    """
    print(f"[下载] 准备下载...")
    print(f"  链接: {share_url}")
    print(f"  密码: {password or '无'}")
    print(f"  保存到: {save_dir}")

    # 访问分享页面
    page.goto(share_url)
    time.sleep(3)

    # 如果有密码，输入提取码
    if password:
        try:
            # 查找密码输入框
            pwd_input = page.query_selector('input[placeholder*="提取码"]')
            if pwd_input:
                pwd_input.fill(password)
                time.sleep(1)

                # 点击确定
                submit_btn = page.query_selector('button:has-text("确定")')
                if submit_btn:
                    submit_btn.click()
                    time.sleep(3)
                    print("[提取码] 已输入")
        except Exception as e:
            print(f"[警告] 提取码输入失败: {e}")

    # 获取文件列表
    print("[解析] 正在获取文件列表...")

    # 这里需要根据实际页面结构定位下载按钮
    # 由于夸克网盘页面可能有反爬，建议：
    # 1. 先转存到网盘（保存按钮）
    # 2. 再从网盘下载

    print("[提示] 由于页面限制，建议先转存到网盘")
    print("[提示] 点击页面上的'保存到网盘'按钮")
    print("[提示] 然后从网盘界面下载")

    # 等待用户手动操作
    input("\n按 Enter 继续（转存完成后）...")

    return True

def main():
    if len(sys.argv) < 3:
        print("用法: python auto_download_cdp.py <分享链接> <保存目录> [提取码]")
        print()
        print("示例:")
        print('  python auto_download_cdp.py "https://pan.quark.cn/s/xxx" "~/Downloads" "密码"')
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)

    print("=" * 80)
    print("夸克网盘自动下载工具 (Chrome CDP 版本)")
    print("=" * 80)
    print()

    with sync_playwright() as p:
        # 启动 Chrome（非 headless，用户可见）
        print("[浏览器] 正在启动 Chrome...")
        browser = p.chromium.launch(
            headless=False,
            channel='chrome',  # 使用系统 Chrome
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ]
        )

        context = browser.new_context(
            viewport=None,  # 使用窗口大小
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )

        page = context.new_page()

        # 访问夸克网盘登录页
        print("[访问] 正在打开夸克网盘...")
        page.goto('https://pan.quark.cn')
        time.sleep(2)

        # 等待用户登录
        if not wait_for_login(page, timeout=300):
            print("[失败] 登录超时")
            browser.close()
            sys.exit(1)

        # 保存 cookie
        cookie_str = save_cookies_playwright_format(page)

        # 下载文件
        success = download_from_share(page, share_url, password, save_dir)

        print()
        print("[完成] 浏览器将保持打开，按 Enter 关闭...")
        input()

        browser.close()

        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
