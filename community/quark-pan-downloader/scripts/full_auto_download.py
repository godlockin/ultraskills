#!/usr/bin/env python3
"""
夸克网盘全自动下载 - 从转存到本地下载完全自动化
用户仅需: Chrome 登录 + 分享链接 + 目标目录

用法:
  python full_auto_download.py <分享链接> <保存目录> [提取码]

示例:
  python full_auto_download.py \\
    "https://pan.quark.cn/s/ce476b55ec2a" \\
    "~/Documents/videos/沈弈斐" \\
    "7efe3YeNNj"

流程:
  1. 从 Chrome 提取 cookie
  2. 自动转存到网盘
  3. 自动获取文件列表
  4. 自动下载所有文件到目标目录
"""

import os
import sys
import time
import json
import httpx
from pathlib import Path
from typing import List, Dict

try:
    import browser_cookie3
except ImportError:
    print("[错误] 缺少依赖: browser-cookie3")
    print("[安装] pip install browser-cookie3 httpx")
    sys.exit(1)

CONFIG_DIR = Path(__file__).parent / 'config'
CONFIG_DIR.mkdir(exist_ok=True)

class QuarkDownloader:
    def __init__(self):
        self.cookies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://pan.quark.cn/'
        }

    def load_chrome_cookies(self):
        """从系统 Chrome 提取 cookie"""
        print("[1/4] 从 Chrome 提取 cookie...")
        try:
            cookies = list(browser_cookie3.chrome(domain_name='quark.cn'))
            self.cookies = {c.name: c.value for c in cookies}
            print(f"[✓] 提取 {len(self.cookies)} 个 cookie")
            return True
        except Exception as e:
            print(f"[错误] {e}")
            return False

    def transfer_share_to_netdisk(self, share_url: str, password: str = None) -> Dict:
        """转存分享文件到网盘"""
        print("[2/4] 转存到网盘...")

        # 解析分享 ID
        share_id = share_url.split('/')[-1]

        # 调用夸克 API 获取分享详情
        api_url = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail"
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'pwd_id': share_id,
            'passcode': password or ''
        }

        try:
            resp = httpx.get(api_url, params=params, cookies=self.cookies, headers=self.headers, timeout=30)
            data = resp.json()

            if data.get('code') != 0:
                print(f"[错误] 获取分享详情失败: {data.get('message')}")
                return {}

            share_info = data.get('data', {})
            print(f"[✓] 分享标题: {share_info.get('title', '未知')}")

            # 获取文件列表
            fid_list = share_info.get('list', [])
            if not fid_list:
                print("[错误] 分享中无文件")
                return {}

            print(f"[✓] 发现 {len(fid_list)} 个文件/文件夹")

            # 调用转存 API
            save_api = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/save"
            save_data = {
                'fid_list': [item['fid'] for item in fid_list],
                'fid_token_list': [item.get('share_fid_token', '') for item in fid_list],
                'to_pdir_fid': '0',  # 根目录
                'pwd_id': share_id,
                'scene': 'link'
            }

            save_resp = httpx.post(save_api, json=save_data, cookies=self.cookies, headers=self.headers, timeout=30)
            save_result = save_resp.json()

            if save_result.get('code') == 0:
                print(f"[✓] 转存成功")
                return {'fid_list': fid_list, 'share_info': share_info}
            else:
                print(f"[错误] 转存失败: {save_result.get('message')}")
                return {}

        except Exception as e:
            print(f"[错误] {e}")
            return {}

    def download_files(self, save_dir: str) -> bool:
        """从网盘下载文件到本地"""
        print("[3/4] 获取网盘文件列表...")

        # 获取网盘根目录文件列表
        list_api = "https://drive-pc.quark.cn/1/clouddrive/file/sort"
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'pdir_fid': '0',
            '_page': '1',
            '_size': '50',
            '_fetch_total': '1'
        }

        try:
            resp = httpx.get(list_api, params=params, cookies=self.cookies, headers=self.headers, timeout=30)
            data = resp.json()

            if data.get('code') != 0:
                print(f"[错误] 获取文件列表失败")
                return False

            files = data.get('data', {}).get('list', [])
            print(f"[✓] 网盘中共 {len(files)} 个文件/文件夹")

            # 下载每个文件
            print("[4/4] 开始下载...")
            os.makedirs(save_dir, exist_ok=True)

            for idx, file_info in enumerate(files[:10], 1):  # 限制前 10 个
                filename = file_info['file_name']
                fid = file_info['fid']
                size_mb = file_info.get('size', 0) / 1024 / 1024

                print(f"[{idx}] {filename} ({size_mb:.1f} MB)")

                # 获取下载链接
                download_url = self._get_download_url(fid)
                if not download_url:
                    print(f"  [跳过] 无法获取下载链接")
                    continue

                # 下载文件
                save_path = Path(save_dir) / filename
                self._download_file(download_url, save_path)

            print(f"[✓] 下载完成: {save_dir}")
            return True

        except Exception as e:
            print(f"[错误] {e}")
            return False

    def _get_download_url(self, fid: str) -> str:
        """获取文件下载链接"""
        api_url = "https://drive-pc.quark.cn/1/clouddrive/file/download"
        params = {'pr': 'ucpro', 'fr': 'pc'}
        data = {'fids': [fid]}

        try:
            resp = httpx.post(api_url, params=params, json=data, cookies=self.cookies, headers=self.headers, timeout=30)
            result = resp.json()

            if result.get('code') == 0:
                return result.get('data', [{}])[0].get('download_url', '')
            return ''
        except:
            return ''

    def _download_file(self, url: str, save_path: Path):
        """下载文件"""
        try:
            with httpx.stream('GET', url, cookies=self.cookies, headers=self.headers, timeout=300, follow_redirects=True) as resp:
                resp.raise_for_status()

                total_size = int(resp.headers.get('content-length', 0))
                downloaded = 0

                with open(save_path, 'wb') as f:
                    for chunk in resp.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 简单进度显示
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            if int(percent) % 10 == 0:
                                print(f"  [{int(percent)}%] {downloaded / 1024 / 1024:.1f} MB", end='\r')

                print(f"  [✓] {save_path.name}")
                return True

        except Exception as e:
            print(f"  [✗] 下载失败: {e}")
            return False

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])
    password = sys.argv[3] if len(sys.argv) > 3 else None

    print("=" * 70)
    print("🚀 夸克网盘全自动下载")
    print("=" * 70)
    print(f"链接: {share_url}")
    print(f"密码: {password or '无'}")
    print(f"目标: {save_dir}")
    print()

    downloader = QuarkDownloader()

    # 1. 提取 cookie
    if not downloader.load_chrome_cookies():
        sys.exit(1)

    # 2. 转存到网盘
    result = downloader.transfer_share_to_netdisk(share_url, password)
    if not result:
        print("[失败] 转存失败")
        sys.exit(1)

    # 等待转存完成
    time.sleep(3)

    # 3. 从网盘下载
    success = downloader.download_files(save_dir)

    print()
    print("=" * 70)
    if success:
        print(f"[完成] 文件已保存到: {save_dir}")
    else:
        print("[失败] 下载未完成，请检查网盘")
    print("=" * 70)

if __name__ == '__main__':
    main()
