#!/usr/bin/env python3
"""
自动化下载脚本 - 绕过交互式输入
基于 quark.py 的批量下载功能
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入原始模块
from quark import QuarkPan

def auto_download(share_url: str, save_dir: str, password: str = None):
    """
    自动下载夸克网盘分享链接

    Args:
        share_url: 分享链接
        save_dir: 保存目录
        password: 提取码（可选）
    """
    print(f"[开始下载]")
    print(f"  链接: {share_url}")
    print(f"  密码: {password or '无'}")
    print(f"  目标: {save_dir}")

    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)

    # 初始化夸克网盘客户端
    try:
        qp = QuarkPan()

        # 读取 cookie
        cookie_file = Path(__file__).parent / 'config' / 'cookies.txt'
        if cookie_file.exists():
            with open(cookie_file) as f:
                cookie_str = f.read().strip()
                qp.load_cookie(cookie_str)
                print("[Cookie] 加载成功")
        else:
            print("[错误] cookies.txt 不存在，请先配置")
            return False

        # 解析分享链接
        print("[解析] 正在获取文件列表...")
        file_list = qp.get_share_files(share_url, password)

        if not file_list:
            print("[错误] 未找到文件或链接失效")
            return False

        print(f"[发现] {len(file_list)} 个文件")

        # 批量下载
        for idx, file_info in enumerate(file_list, 1):
            filename = file_info['file_name']
            size = file_info.get('size', 0)
            size_mb = size / 1024 / 1024

            print(f"[{idx}/{len(file_list)}] {filename} ({size_mb:.1f} MB)")

            # 下载文件
            save_path = os.path.join(save_dir, filename)
            success = qp.download_file(file_info, save_path)

            if success:
                print(f"  ✓ 完成: {save_path}")
            else:
                print(f"  ✗ 失败: {filename}")

        print(f"\n[全部完成] 保存到: {save_dir}")
        return True

    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # 从 url.txt 读取链接
    url_file = Path(__file__).parent / 'config' / 'url.txt'

    if not url_file.exists():
        print("[错误] config/url.txt 不存在")
        sys.exit(1)

    with open(url_file) as f:
        url_line = f.read().strip()

    # 解析链接和密码
    if '?pwd=' in url_line:
        share_url, pwd_part = url_line.split('?pwd=')
        password = pwd_part
    else:
        share_url = url_line
        password = None

    # 保存目录（从命令行参数或默认）
    save_dir = sys.argv[1] if len(sys.argv) > 1 else './downloads'

    # 执行下载
    success = auto_download(share_url, save_dir, password)
    sys.exit(0 if success else 1)
