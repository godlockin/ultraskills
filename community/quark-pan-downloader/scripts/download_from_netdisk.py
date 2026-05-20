#!/usr/bin/env python3
"""
从夸克网盘下载已转存的文件
适用于文件已在网盘中的场景

用法:
  python download_from_netdisk.py <网盘文件名或关键词> <保存目录>

示例:
  python download_from_netdisk.py "沈弈斐" "~/Documents/videos/沈弈斐"
"""

import os
import sys
import asyncio
import httpx
from pathlib import Path

try:
    import browser_cookie3
except ImportError:
    print("pip install browser-cookie3 httpx")
    sys.exit(1)

def get_timestamp(length=10):
    import random, time
    ts = str(int(time.time() * 1000))
    return ts[:length] if length < 13 else ts + str(random.randint(100, 999))

class QuarkNetdiskDownloader:
    def __init__(self):
        cookies = list(browser_cookie3.chrome(domain_name='quark.cn'))
        self.cookie_str = '; '.join([f"{c.name}={c.value}" for c in cookies])
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'origin': 'https://pan.quark.cn',
            'referer': 'https://pan.quark.cn/',
            'cookie': self.cookie_str
        }
        print(f"[Cookie] 已加载 {len(cookies)} 个")

    async def list_files(self, pdir_fid='0'):
        """列出网盘文件"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/file/sort'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'pdir_fid': pdir_fid,
            '_page': '1',
            '_size': '100',
            '_sort': 'update_at:desc'
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(api, params=params, headers=self.headers, timeout=30)
            data = resp.json()
            return data.get('data', {}).get('list', [])

    async def get_download_url(self, fid: str):
        """获取单个文件下载链接"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/file/download'
        params = {'pr': 'ucpro', 'fr': 'pc'}
        data = {'fids': [fid]}

        async with httpx.AsyncClient() as client:
            resp = await client.post(api, json=data, headers=self.headers, params=params, timeout=60)
            result = resp.json()

            if result.get('status') == 200 and result.get('data'):
                return result['data'][0].get('download_url', '')
            return ''

    async def download_file(self, url: str, save_path: Path):
        """下载文件"""
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url, headers=self.headers, timeout=600, follow_redirects=True) as resp:
                resp.raise_for_status()

                total = int(resp.headers.get('content-length', 0))
                downloaded = 0

                with open(save_path, 'wb') as f:
                    async for chunk in resp.aiter_bytes(chunk_size=1024*1024):
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total > 0:
                            percent = (downloaded / total) * 100
                            mb = downloaded / 1024 / 1024
                            total_mb = total / 1024 / 1024
                            print(f"  [{int(percent)}%] {mb:.1f}/{total_mb:.1f} MB", end='\r')

                print(f"\n  [✓] {save_path.name} ({total / 1024 / 1024:.1f} MB)")

    async def download_folder(self, folder_fid: str, folder_name: str, save_dir: Path):
        """递归下载文件夹"""
        print(f"  [文件夹] 进入: {folder_name}")

        # 创建子目录
        folder_path = save_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        # 获取文件夹内容
        files = await self.list_files(folder_fid)

        if not files:
            print(f"  [空] 文件夹为空")
            return

        print(f"  [→] 发现 {len(files)} 个文件")

        for f in files:
            fname = f['file_name']
            fid = f['fid']
            is_dir = f.get('dir', False)

            if is_dir:
                # 递归下载子文件夹
                await self.download_folder(fid, fname, folder_path)
            else:
                # 下载文件
                print(f"    [下载] {fname}")
                download_url = await self.get_download_url(fid)

                if download_url:
                    await self.download_file(download_url, folder_path / fname)
                else:
                    print(f"    [失败] {fname}")

    async def download_by_keyword(self, keyword: str, save_dir: str):
        """根据关键词搜索并下载网盘文件"""
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)

        # 1. 列出网盘文件
        print(f"[1/3] 搜索网盘文件（关键词: {keyword})...")
        files = await self.list_files('0')

        # 2. 匹配关键词
        matched = [f for f in files if keyword.lower() in f['file_name'].lower()]

        if not matched:
            print(f"[错误] 未找到包含'{keyword}'的文件")
            print(f"[提示] 网盘中共 {len(files)} 个文件，最近的:")
            for f in files[:5]:
                print(f"  - {f['file_name']}")
            return False

        print(f"[✓] 找到 {len(matched)} 个匹配文件:")
        for f in matched:
            size_mb = f.get('size', 0) / 1024 / 1024
            print(f"  - {f['file_name']} ({size_mb:.1f} MB)")

        # 3. 下载所有匹配文件
        print(f"\n[2/3] 开始下载...")

        for idx, file_info in enumerate(matched, 1):
            filename = file_info['file_name']
            fid = file_info['fid']
            is_dir = file_info.get('dir', False)

            print(f"\n[{idx}/{len(matched)}] {filename}")

            if is_dir:
                print(f"  [文件夹] {filename}")
                # 递归下载文件夹
                await self.download_folder(fid, filename, save_path)
                continue

            # 获取下载链接
            download_url = await self.get_download_url(fid)

            if not download_url:
                print(f"  [失败] 无法获取下载链接")
                continue

            # 下载
            local_path = save_path / filename
            await self.download_file(download_url, local_path)

        print(f"\n[3/3] 完成!")
        print(f"[✓] 保存到: {save_dir}")
        return True

async def main_async():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    keyword = sys.argv[1]
    save_dir = os.path.expanduser(sys.argv[2])

    print("=" * 70)
    print("🚀 夸克网盘下载（从网盘）")
    print("=" * 70)
    print()

    downloader = QuarkNetdiskDownloader()
    success = await downloader.download_by_keyword(keyword, save_dir)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    asyncio.run(main_async())
