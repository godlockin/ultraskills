#!/usr/bin/env python3
"""
夸克网盘完全自动下载 - 基于原 quark.py 的核心代码
从 Chrome 提取 cookie → 转存 → 下载到本地

用法:
  python fully_auto.py <分享链接> <保存目录> [提取码]
"""

import os
import sys
import time
import json
import asyncio
import httpx
from pathlib import Path

try:
    import browser_cookie3
except ImportError:
    print("pip install browser-cookie3 httpx")
    sys.exit(1)

def get_timestamp(length=10):
    """生成时间戳"""
    import random
    ts = str(int(time.time() * 1000))
    return ts[:length] if length < 13 else ts + str(random.randint(100, 999))

class QuarkAuto:
    def __init__(self):
        # 从 Chrome 提取 cookie
        cookies = list(browser_cookie3.chrome(domain_name='quark.cn'))
        self.cookie_str = '; '.join([f"{c.name}={c.value}" for c in cookies])
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'origin': 'https://pan.quark.cn',
            'referer': 'https://pan.quark.cn/',
            'cookie': self.cookie_str
        }
        print(f"[Cookie] 已加载 {len(cookies)} 个")

    async def get_stoken(self, pwd_id: str, password: str = ''):
        """获取 stoken（转存和访问分享需要）"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            '__dt': get_timestamp(4),
            '__t': get_timestamp(13)
        }
        data = {'pwd_id': pwd_id, 'passcode': password}

        async with httpx.AsyncClient() as client:
            resp = await client.post(api, json=data, params=params, headers=self.headers, timeout=30)
            result = resp.json()

            if result.get('status') == 200 and result.get('data'):
                return result['data']['stoken']
            else:
                print(f"[错误] 获取 stoken 失败: {result.get('message')}")
                return ''

    async def get_share_info(self, pwd_id: str, stoken: str, passcode: str = ''):
        """获取分享详情（需要 stoken）"""
    async def get_share_info(self, pwd_id: str, stoken: str, passcode: str = ''):
        """获取分享详情（需要 stoken）"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'pwd_id': pwd_id,
            'stoken': stoken,
            'pdir_fid': '0',
            '_page': '1',
            '_size': '50'
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(api, params=params, headers=self.headers, timeout=30)
            data = resp.json()

            if data.get('code') != 0:
                print(f"[错误] {data.get('message')}")
                return None

            return data['data']

    async def transfer_to_netdisk(self, pwd_id: str, stoken: str, fid_list: list, fid_tokens: list):
        """转存到网盘"""
        api = 'https://drive.quark.cn/1/clouddrive/share/sharepage/save'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            '__dt': get_timestamp(4),
            '__t': get_timestamp(13)
        }
        data = {
            'fid_list': fid_list,
            'fid_token_list': fid_tokens,
            'to_pdir_fid': '0',
            'pwd_id': pwd_id,
            'stoken': stoken,
            'pdir_fid': '0',
            'scene': 'link'
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(api, json=data, headers=self.headers, params=params, timeout=60)
            result = resp.json()

            if result.get('code') == 0:
                task_id = result['data']['task_id']
                print(f"[转存] 任务ID: {task_id}")
                return await self.wait_task(task_id)
            else:
                print(f"[错误] {result.get('message')}")
                return False

    async def wait_task(self, task_id: str, max_retry=50):
        """等待任务完成"""
        api = 'https://drive.quark.cn/1/clouddrive/task'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'task_id': task_id,
            '__dt': get_timestamp(4),
            '__t': get_timestamp(13)
        }

        import random
        for i in range(max_retry):
            await asyncio.sleep(random.randint(500, 1000) / 1000)

            async with httpx.AsyncClient() as client:
                resp = await client.get(api, params=params, headers=self.headers, timeout=30)
                data = resp.json()

                status = data.get('data', {}).get('status')
                if status == 2:
                    print(f"[✓] 转存完成")
                    return True
                elif status in [3, 4]:
                    print(f"[失败] 任务失败")
                    return False

                if (i + 1) % 5 == 0:
                    print(f"[等待] 转存中... ({i+1}/{max_retry})")

        return False

    async def get_netdisk_files(self, pdir_fid='0'):
        """获取网盘文件列表"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/file/sort'
        params = {
            'pr': 'ucpro',
            'fr': 'pc',
            'pdir_fid': pdir_fid,
            '_page': '1',
            '_size': '100',
            '_fetch_total': '1'
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(api, params=params, headers=self.headers, timeout=30)
            data = resp.json()

            if data.get('code') == 0:
                return data['data']['list']
            return []

    async def get_download_urls(self, fid_list: list):
        """获取文件下载链接"""
        api = 'https://drive-pc.quark.cn/1/clouddrive/file/download'
        params = {'pr': 'ucpro', 'fr': 'pc'}
        data = {'fids': fid_list}

        async with httpx.AsyncClient() as client:
            resp = await client.post(api, json=data, headers=self.headers, params=params, timeout=60)
            result = resp.json()

            if result.get('status') == 200:
                return result.get('data', [])
            else:
                print(f"[错误] 获取下载链接失败: {result.get('message')}")
                return []

    async def download_file(self, url: str, save_path: str):
        """下载单个文件"""
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url, headers=self.headers, timeout=300, follow_redirects=True) as resp:
                resp.raise_for_status()

                total = int(resp.headers.get('content-length', 0))
                downloaded = 0

                with open(save_path, 'wb') as f:
                    async for chunk in resp.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total > 0 and downloaded % (1024 * 1024) == 0:
                            percent = (downloaded / total) * 100
                            print(f"  [{int(percent)}%] {downloaded / 1024 / 1024:.1f} MB", end='\r')

                print(f"  [✓] {Path(save_path).name}")

    async def auto_download(self, share_url: str, save_dir: str, password: str = None):
        """完全自动化：转存 + 下载"""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        # 解析分享 ID
        pwd_id = share_url.split('/')[-1].split('?')[0]

        # 1. 获取 stoken
        print(f"[1/5] 获取 stoken... (ID: {pwd_id})")
        stoken = await self.get_stoken(pwd_id, password or '')

        if not stoken:
            return False

        print(f"[✓] stoken: {stoken[:20]}...")

        # 2. 获取分享详情
        print(f"[2/5] 获取分享详情...")
        share_info = await self.get_share_info(pwd_id, stoken, password or '')

        if not share_info:
            return False

        stoken = share_info.get('stoken', '')
        file_list = share_info.get('list', [])

        if not file_list:
            print("[错误] 分享中无文件")
            return False

        print(f"[✓] 标题: {share_info.get('title', '未知')}")
        print(f"[✓] 文件数: {len(file_list)}")

        # 3. 转存到网盘
        print(f"[3/5] 转存到网盘...")
        fid_list = [f['fid'] for f in file_list]
        fid_tokens = [f.get('share_fid_token', '') for f in file_list]

        success = await self.transfer_to_netdisk(pwd_id, stoken, fid_list, fid_tokens)

        if not success:
            return False

        # 等待文件在网盘中可见
        await asyncio.sleep(2)

        # 4. 从网盘获取文件列表
        print(f"[4/5] 获取网盘文件...")
        netdisk_files = await self.get_netdisk_files('0')

        # 找到刚转存的文件（通过标题匹配）
        share_title = share_info.get('title', '')
        target_files = []

        for f in netdisk_files:
            if share_title in f.get('file_name', ''):
                target_files.append(f)
            elif any(item['fid'] in f.get('fid', '') for item in file_list[:3]):
                target_files.append(f)

        if not target_files:
            # 使用最近的文件（按修改时间）
            target_files = sorted(netdisk_files, key=lambda x: x.get('updated_at', 0), reverse=True)[:len(file_list)]

        print(f"[✓] 找到 {len(target_files)} 个目标文件")

        # 5. 获取下载链接并下载
        print(f"[5/5] 下载到本地...")

        download_fids = [f['fid'] for f in target_files if not f.get('dir', False)]  # 只下载文件，跳过文件夹

        if not download_fids:
            print("[警告] 只有文件夹，需要递归下载（暂不支持）")
            print(f"[提示] 请手动在网盘中下载: https://pan.quark.cn")
            return False

        download_infos = await self.get_download_urls(download_fids)

        for info in download_infos:
            filename = info['file_name']
            download_url = info['download_url']
            save_path = save_dir / filename

            print(f"[下载] {filename}")
            await self.download_file(download_url, str(save_path))

        print(f"[✓] 全部下载到: {save_dir}")
        return True

async def main_async():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    share_url = sys.argv[1]
    save_dir = sys.argv[2]
    password = sys.argv[3] if len(sys.argv) > 3 else None

    print("=" * 70)
    print("🚀 夸克网盘完全自动下载")
    print("=" * 70)
    print()

    downloader = QuarkAuto()
    success = await downloader.auto_download(share_url, save_dir, password)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    asyncio.run(main_async())
