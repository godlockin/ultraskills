#!/usr/bin/env python3
"""
Playwright Media Sniffer - 浏览器自动化媒体嗅探器

Usage:
    python sniff_and_download.py <url> [--auth-state <path>] [--browser chrome|firefox] [--headless]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# 配置
DOWNLOADS_DIR = Path.home() / "Downloads" / "media-sniffer"
AUTH_DIR = Path(__file__).parent.parent / "auth"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
AUTH_DIR.mkdir(parents=True, exist_ok=True)


class MediaSniffer:
    def __init__(self, target_url, auth_state=None, browser_type='chromium', headless=False):
        self.target_url = target_url
        self.auth_state = auth_state
        self.browser_type = browser_type
        self.headless = headless
        self.captured_resources = []

    def on_request(self, request):
        """监听网络请求"""
        url = request.url

        # 筛选媒体资源
        media_patterns = [
            r'\.m3u8',
            r'\.mpd',
            r'\.mp4',
            r'\.ts$',
            r'\.m4s',
            r'\.webm',
            r'\.flv',
            r'audio/',
            r'video/'
        ]

        if any(re.search(pattern, url, re.I) for pattern in media_patterns):
            # 过滤分片文件（只要主清单）
            if re.search(r'\d+\.ts$', url) or re.search(r'segment\d+', url):
                return

            self.captured_resources.append({
                'url': url,
                'type': request.resource_type,
                'method': request.method,
                'headers': dict(request.headers)
            })
            print(f"🎯 Captured: {url[:80]}...")

    def prioritize_resources(self):
        """智能排序资源"""
        scored = []
        for r in self.captured_resources:
            url = r['url']
            score = 0

            # M3U8/MPD 主清单优先
            if re.search(r'(index|master|playlist).*\.m3u8', url, re.I):
                score += 10
            elif '.m3u8' in url:
                score += 5
            elif '.mpd' in url:
                score += 10

            # 直接 MP4
            if '.mp4' in url and 'segment' not in url:
                score += 7

            # 避免缩略图/预览
            if 'thumb' in url or 'preview' in url or 'poster' in url:
                score -= 5

            scored.append((score, r))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [r for _, r in scored]

    def sniff(self):
        """执行嗅探"""
        with sync_playwright() as p:
            # 选择浏览器
            if self.browser_type == 'firefox':
                browser = p.firefox.launch(headless=self.headless)
            else:
                browser = p.chromium.launch(headless=self.headless)

            # 创建上下文（加载登录态）
            context_options = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'viewport': {'width': 1920, 'height': 1080},
                'locale': 'zh-CN',
                'timezone_id': 'Asia/Shanghai',
            }

            if self.auth_state and Path(self.auth_state).exists():
                context_options['storage_state'] = self.auth_state
                print(f"✅ Loaded auth state: {self.auth_state}")
            else:
                print("ℹ️  No auth state provided, using anonymous session")

            context = browser.new_context(**context_options)
            page = context.new_page()

            # 监听网络请求
            page.on('request', self.on_request)

            # 打开目标页面
            print(f"🌐 Opening: {self.target_url}")
            try:
                page.goto(self.target_url, wait_until='networkidle', timeout=30000)
            except Exception as e:
                print(f"⚠️  Page load timeout: {e}")

            # 等待视频播放器加载
            print("⏳ Waiting for player to load...")
            page.wait_for_timeout(3000)

            # 尝试点击播放按钮
            try:
                play_selectors = [
                    'button:has-text("播放")',
                    'button:has-text("Play")',
                    'button[aria-label*="play" i]',
                    '.video-play-btn',
                    '.play-button',
                    'video'
                ]

                for selector in play_selectors:
                    try:
                        element = page.locator(selector).first
                        if element.is_visible(timeout=1000):
                            element.click()
                            print(f"▶️  Clicked play button: {selector}")
                            break
                    except:
                        continue

                # 等待视频开始播放（触发更多请求）
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"ℹ️  No play button found: {e}")

            # 最终等待
            page.wait_for_timeout(2000)

            # 关闭
            browser.close()

            print(f"\n✅ Captured {len(self.captured_resources)} resources")
            return self.prioritize_resources()


def extract_cookies_from_browser(domain, browser='chrome'):
    """从本地浏览器提取 cookies"""
    try:
        import browser_cookie3

        if browser == 'chrome':
            cookies = browser_cookie3.chrome(domain_name=domain)
        elif browser == 'firefox':
            cookies = browser_cookie3.firefox(domain_name=domain)
        elif browser == 'edge':
            cookies = browser_cookie3.edge(domain_name=domain)
        else:
            cookies = browser_cookie3.load(domain_name=domain)

        return list(cookies)
    except Exception as e:
        print(f"⚠️  Failed to extract cookies: {e}")
        print(f"   Install: pip install browser-cookie3")
        return []


def download_resource(resource, target_url, output_dir):
    """使用 yt-dlp 或 ffmpeg 下载资源"""
    url = resource['url']
    headers = resource['headers']

    # 提取文件名
    domain = urlparse(target_url).netloc.replace('.', '_')
    timestamp = int(time.time())

    # 构造 yt-dlp 命令
    cmd = [
        'yt-dlp',
        '--no-check-certificate',
        '--add-header', f'Referer: {target_url}',
        '--add-header', f'User-Agent: {headers.get("user-agent", "")}',
        '--output', f'{output_dir}/{domain}_{timestamp}_%(title)s.%(ext)s',
        url
    ]

    # 添加 cookies（如果有）
    if 'cookie' in headers:
        cmd.extend(['--add-header', f'Cookie: {headers["cookie"]}'])

    print(f"\n📥 Downloading with yt-dlp...")
    print(f"   URL: {url[:60]}...")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Download successful!")
        return True
    else:
        print(f"⚠️  yt-dlp failed: {result.stderr[:200]}")
        print(f"\n🔄 Trying ffmpeg...")

        # Fallback: ffmpeg
        output_file = f'{output_dir}/{domain}_{timestamp}.mp4'
        headers_str = '\r\n'.join([f'{k}: {v}' for k, v in headers.items()])

        cmd_ffmpeg = [
            'ffmpeg',
            '-headers', headers_str,
            '-i', url,
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            output_file
        ]

        result = subprocess.run(cmd_ffmpeg, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ ffmpeg download successful: {output_file}")
            return True
        else:
            print(f"❌ ffmpeg also failed: {result.stderr[:200]}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Playwright Media Sniffer')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('--auth-state', help='Path to auth state JSON')
    parser.add_argument('--browser', choices=['chrome', 'chromium', 'firefox'], default='chromium')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--login-first', action='store_true', help='Manual login before sniffing')
    parser.add_argument('--output', default=str(DOWNLOADS_DIR), help='Output directory')

    args = parser.parse_args()

    # 登录模式
    if args.login_first:
        print("🔐 Login mode: Please login manually in the browser")
        domain = urlparse(args.url).netloc
        auth_file = AUTH_DIR / f'{domain.replace(".", "_")}.json'

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(args.url)

            input("\n⏸️  Press Enter after you've logged in...")

            # 保存登录态
            context.storage_state(path=str(auth_file))
            print(f"✅ Auth state saved: {auth_file}")
            browser.close()

        print(f"\n💡 Next time, use: --auth-state {auth_file}")
        return

    # 嗅探
    sniffer = MediaSniffer(
        target_url=args.url,
        auth_state=args.auth_state,
        browser_type=args.browser,
        headless=args.headless
    )

    resources = sniffer.sniff()

    if not resources:
        print("\n❌ No media resources found!")
        print("💡 Try:")
        print("   1. Use --login-first if the page requires authentication")
        print("   2. Wait longer (video might load slowly)")
        print("   3. Check if the page uses DRM (Widevine/FairPlay)")
        return 1

    # 显示候选资源
    print("\n" + "=" * 80)
    print("📋 Captured Media Resources:")
    print("=" * 80)
    for i, res in enumerate(resources[:5], 1):
        url_display = res['url'][:70]
        print(f"{i}. [{res['type']}] {url_display}...")

    # 选择下载
    if len(resources) == 1:
        choice = 0
    else:
        try:
            choice_input = input(f"\nSelect resource to download (1-{min(5, len(resources))}, Enter for #1): ").strip()
            choice = int(choice_input) - 1 if choice_input else 0
        except ValueError:
            choice = 0

    selected = resources[choice]

    # 下载
    success = download_resource(selected, args.url, args.output)

    # 保存元数据
    metadata = {
        'target_url': args.url,
        'captured_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'resource_url': selected['url'],
        'resource_type': selected['type'],
        'headers': selected['headers'],
        'total_candidates': len(resources)
    }

    metadata_file = Path(args.output) / f'metadata_{int(time.time())}.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Metadata saved: {metadata_file}")

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
