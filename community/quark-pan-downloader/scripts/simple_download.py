#!/usr/bin/env python3
"""
夸克网盘一键下载 - 简化版
用户只需: 1) 在 Chrome 中登录 2) 提供链接 3) 指定目录

用法:
  python simple_download.py <分享链接> <保存目录> [提取码]

示例:
  python simple_download.py \\
    "https://pan.quark.cn/s/ce476b55ec2a" \\
    "~/Documents/videos/沈弈斐" \\
    "7efe3YeNNj"
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    import browser_cookie3
except ImportError:
    print("[错误] 缺少依赖: browser-cookie3")
    print("[安装] pip install --system browser-cookie3")
    sys.exit(1)

CONFIG_DIR = Path(__file__).parent / 'config'

def extract_cookies(domain='quark.cn'):
    """提取 Chrome cookie"""
    try:
        cookies = list(browser_cookie3.chrome(domain_name=domain))
        if not cookies:
            return None

        # Playwright 格式
        playwright_fmt = []
        for c in cookies:
            playwright_fmt.append({
                'name': c.name,
                'value': c.value,
                'domain': c.domain,
                'path': c.path
            })

        # 保存
        cookie_file = CONFIG_DIR / 'cookies.txt'
        with open(cookie_file, 'w') as f:
            f.write(str(playwright_fmt))

        return len(cookies)

    except Exception as e:
        print(f"[错误] {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    os.makedirs(save_dir, exist_ok=True)

    print("🚀 夸克网盘一键下载")
    print("=" * 60)
    print()

    # Step 1: 提取 cookie
    print("[1/2] 从 Chrome 提取 cookie...")
    cookie_count = extract_cookies()

    if not cookie_count:
        print("[失败] 请先在 Chrome 中登录 https://pan.quark.cn")
        sys.exit(1)

    print(f"[✓] 提取 {cookie_count} 个 cookie")
    print()

    # Step 2: 在浏览器中打开分享链接
    print("[2/2] 正在打开分享页面...")
    full_url = f"{share_url}?pwd={password}" if password else share_url

    subprocess.run(['open', full_url], check=False)

    print(f"[✓] 已在浏览器中打开")
    print()
    print("=" * 60)
    print("📱 请在浏览器中完成:")
    print()
    print("  1️⃣  点击'保存到网盘'按钮")
    print("  2️⃣  (可选) 选择保存位置")
    print("  3️⃣  等待转存完成")
    print("  4️⃣  打开网盘: https://pan.quark.cn")
    print("  5️⃣  找到刚转存的文件夹")
    print("  6️⃣  全选文件 → 下载")
    print("  7️⃣  下载完成后移动到:")
    print(f"      {save_dir}")
    print()
    print("=" * 60)
    print()
    print("💡 提示:")
    print("  - 转存后分享链接失效也能下载")
    print("  - 大文件（>5GB）可能需要夸克 APP 下载")
    print("  - Cookie 有效期约 30 天")
    print()
    print(f"[完成] Cookie 已保存到: {CONFIG_DIR / 'cookies.txt'}")
    print(f"[目标] 文件最终保存到: {save_dir}")

if __name__ == '__main__':
    main()
