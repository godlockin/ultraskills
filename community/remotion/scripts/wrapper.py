#!/usr/bin/env python3
"""
Remotion skill wrapper — 对 Remotion CLI 的薄封装。

本脚本不重新实现 Remotion,只做三件事:
  1. 预检环境(node / npm / ffmpeg / 磁盘空间)
  2. 把常用操作收敛成一条命令(init / render / studio / preflight)
  3. 在渲染前给出并发与内存的合理默认值

Usage:
    python3 wrapper.py preflight
    python3 wrapper.py init <project-dir> [--template <name>]
    python3 wrapper.py studio [--dir <project-dir>]
    python3 wrapper.py render <composition> <output> [--dir <project-dir>]
                              [--concurrency N] [--scale S] [--frames A-B]
                              [--props <json-or-file>] [--codec <codec>]

Exit codes:
    0 = 成功
    1 = 命令执行失败
    2 = 参数错误
    3 = 预检未通过(缺依赖 / 磁盘不足)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 渲染 1080p 时每个 Chrome 实例的经验内存占用(GB)
RAM_PER_WORKER_GB = 1.5
# 长渲染建议的最小空闲磁盘(GB)
MIN_FREE_DISK_GB = 5


def _run(cmd: list[str], cwd: Path | None = None) -> int:
    """执行命令,继承 stdio。返回 exit code。"""
    print(f"$ {' '.join(cmd)}", file=sys.stderr)
    try:
        return subprocess.run(cmd, cwd=cwd, check=False).returncode
    except FileNotFoundError:
        print(f"错误: 找不到可执行文件 {cmd[0]}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("已中断", file=sys.stderr)
        return 130


def _which(name: str) -> str | None:
    return shutil.which(name)


def _node_major() -> int | None:
    node = _which("node")
    if not node:
        return None
    try:
        out = subprocess.run(
            [node, "--version"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None
    # v20.11.0 -> 20
    try:
        return int(out.lstrip("v").split(".")[0])
    except (ValueError, IndexError):
        return None


def _free_disk_gb(path: Path) -> float:
    try:
        usage = shutil.disk_usage(path)
    except OSError:
        return -1.0
    return usage.free / (1024**3)


def _suggested_concurrency() -> int:
    cores = os.cpu_count() or 4
    return max(1, cores // 2)


def cmd_preflight(args: argparse.Namespace) -> int:
    """渲染前的环境预检 — 长渲染动辄数小时,先花 2 秒确认环境。"""
    problems: list[str] = []
    notes: list[str] = []

    major = _node_major()
    if major is None:
        problems.append("未找到 node — Remotion 需要 Node.js >= 18")
    elif major < 18:
        problems.append(f"node 版本过低 (v{major}) — Remotion 需要 >= 18")
    else:
        notes.append(f"node v{major} OK")

    if not (_which("npm") or _which("pnpm") or _which("bun")):
        problems.append("未找到 npm / pnpm / bun")
    else:
        notes.append("包管理器 OK")

    if _which("ffmpeg"):
        notes.append("ffmpeg OK (系统级)")
    else:
        notes.append("ffmpeg 未在 PATH — Remotion 会自带,通常无需处理")

    target = Path(args.dir).resolve() if args.dir else Path.cwd()
    free = _free_disk_gb(target)
    if free < 0:
        notes.append("无法读取磁盘剩余空间")
    elif free < MIN_FREE_DISK_GB:
        problems.append(
            f"磁盘剩余 {free:.1f}GB < {MIN_FREE_DISK_GB}GB — 帧序列可能写不下"
        )
    else:
        notes.append(f"磁盘剩余 {free:.1f}GB OK")

    conc = _suggested_concurrency()
    notes.append(
        f"建议 --concurrency {conc} "
        f"(约需 {conc * RAM_PER_WORKER_GB:.1f}GB RAM;OOM 时下调)"
    )

    for n in notes:
        print(f"  ✓ {n}")
    if problems:
        print("Preflight: FAIL")
        for p in problems:
            print(f"  ❌ {p}")
        return 3
    print("Preflight: PASS")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """脚手架 — 委托给官方 create-video。"""
    rc = cmd_preflight(argparse.Namespace(dir=None))
    if rc != 0:
        print("预检未通过,已中止 init", file=sys.stderr)
        return rc

    cmd = ["npx", "create-video@latest", args.project_dir]
    if args.template:
        cmd += ["--template", args.template]
    rc = _run(cmd)
    if rc == 0:
        print(f"\n下一步:\n  cd {args.project_dir}\n  npm run dev")
    return rc


def cmd_studio(args: argparse.Namespace) -> int:
    """启动 Remotion Studio。"""
    cwd = Path(args.dir).resolve() if args.dir else Path.cwd()
    if not (cwd / "package.json").exists():
        print(f"错误: {cwd} 下没有 package.json — 请在 Remotion 项目内运行", file=sys.stderr)
        return 2
    return _run(["npx", "remotion", "studio"], cwd=cwd)


def cmd_render(args: argparse.Namespace) -> int:
    """渲染 — 带上并发/缩放等性能参数。"""
    cwd = Path(args.dir).resolve() if args.dir else Path.cwd()
    if not (cwd / "package.json").exists():
        print(f"错误: {cwd} 下没有 package.json — 请在 Remotion 项目内运行", file=sys.stderr)
        return 2

    rc = cmd_preflight(argparse.Namespace(dir=str(cwd)))
    if rc != 0:
        print("预检未通过,已中止 render", file=sys.stderr)
        return rc

    cmd = ["npx", "remotion", "render", args.composition, args.output]

    concurrency = args.concurrency or _suggested_concurrency()
    cmd += ["--concurrency", str(concurrency)]

    if args.scale:
        cmd += ["--scale", str(args.scale)]
    if args.frames:
        cmd += ["--frames", args.frames]
    if args.codec:
        cmd += ["--codec", args.codec]
    elif args.output.endswith(".gif"):
        # GIF 必须显式指定 codec 与抽帧,否则体积失控
        cmd += ["--codec", "gif", "--every-nth-frame", "2", "--fps", "15"]
    if args.timeout:
        cmd += ["--timeout", str(args.timeout)]
    if args.props:
        props = args.props
        p = Path(props)
        if p.exists():
            props = p.read_text(encoding="utf-8")
        else:
            try:
                json.loads(props)
            except json.JSONDecodeError:
                print(
                    f"错误: --props 既不是存在的文件也不是合法 JSON: {props[:60]}",
                    file=sys.stderr,
                )
                return 2
        cmd += ["--props", props]

    rc = _run(cmd, cwd=cwd)
    if rc != 0:
        print(
            "\n渲染失败。常见原因见 SKILL.md「故障排查」:\n"
            "  - OOM / Chrome crash → 降低 --concurrency 或 --scale\n"
            "  - 字体变成 fallback → 需 loadFont() + waitUntilDone()\n"
            "  - 卡住直到超时 → delayRender 后忘了 continueRender\n",
            file=sys.stderr,
        )
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remotion CLI 薄封装(预检 + 常用操作)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_pre = sub.add_parser("preflight", help="检查 node/包管理器/ffmpeg/磁盘")
    p_pre.add_argument("--dir", help="要检查磁盘空间的目录(默认当前目录)")
    p_pre.set_defaults(func=cmd_preflight)

    p_init = sub.add_parser("init", help="创建 Remotion 项目(委托 create-video)")
    p_init.add_argument("project_dir", help="项目目录名")
    p_init.add_argument("--template", help="create-video 模板名")
    p_init.set_defaults(func=cmd_init)

    p_studio = sub.add_parser("studio", help="启动 Remotion Studio")
    p_studio.add_argument("--dir", help="项目目录(默认当前目录)")
    p_studio.set_defaults(func=cmd_studio)

    p_render = sub.add_parser("render", help="渲染合成")
    p_render.add_argument("composition", help="Composition id")
    p_render.add_argument("output", help="输出文件,如 out.mp4")
    p_render.add_argument("--dir", help="项目目录(默认当前目录)")
    p_render.add_argument("--concurrency", type=int, help="并发 worker 数(默认 cores/2)")
    p_render.add_argument("--scale", type=float, help="分辨率缩放,如 0.5")
    p_render.add_argument("--frames", help="帧范围,如 0-90")
    p_render.add_argument("--codec", help="显式指定 codec")
    p_render.add_argument("--timeout", type=int, help="单帧超时(ms),默认 30000")
    p_render.add_argument("--props", help="input props:JSON 字符串或 .json 文件路径")
    p_render.set_defaults(func=cmd_render)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
