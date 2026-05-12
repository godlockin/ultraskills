#!/usr/bin/env python3
"""
md_render_enhanced.py - 美观交互增强版 Markdown 渲染器

集成设计模式:
- Magazine-web-ppt 的 5 套主题色板
- 响应式 sidebar TOC + 平滑滚动
- Reading progress bar
- Copy code 按钮
- Dark mode 切换
- Print-friendly CSS
- Mermaid/Graphviz SVG 渲染

Usage:
  python3 md_render_enhanced.py input.md
  python3 md_render_enhanced.py input.md --theme indigo
  python3 md_render_enhanced.py input.md --no-toc
  python3 md_render_enhanced.py input.md --inline-svg
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple

try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc, codehilite
except ImportError:
    print("Error: markdown not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)

try:
    from pygments.formatters import HtmlFormatter
except ImportError:
    HtmlFormatter = None


# === 主题色板 (from magazine-web-ppt) ===

THEMES = {
    "monocle": {
        "name": "墨水经典 (Monocle)",
        "description": "纯墨黑 + 暖米白，杂志感最强",
        "ink": "#0a0a0b",
        "ink_rgb": "10,10,11",
        "paper": "#f1efea",
        "paper_rgb": "241,239,234",
        "paper_tint": "#e8e5de",
        "ink_tint": "#18181a",
    },
    "indigo": {
        "name": "靛蓝瓷 (Indigo Porcelain)",
        "description": "深靛蓝 + 瓷白，科技/研究风",
        "ink": "#0a1f3d",
        "ink_rgb": "10,31,61",
        "paper": "#f1f3f5",
        "paper_rgb": "241,243,245",
        "paper_tint": "#e4e8ec",
        "ink_tint": "#152a4a",
    },
    "forest": {
        "name": "森林墨 (Forest Ink)",
        "description": "深森林绿 + 象牙，自然/可持续风",
        "ink": "#1a2e1f",
        "ink_rgb": "26,46,31",
        "paper": "#f5f1e8",
        "paper_rgb": "245,241,232",
        "paper_tint": "#ece7da",
        "ink_tint": "#253d2c",
    },
    "kraft": {
        "name": "牛皮纸 (Kraft Paper)",
        "description": "深棕 + 暖米，怀旧/人文风",
        "ink": "#2a1e13",
        "ink_rgb": "42,30,19",
        "paper": "#eedfc7",
        "paper_rgb": "238,223,199",
        "paper_tint": "#e0d0b6",
        "ink_tint": "#3a2a1d",
    },
    "dune": {
        "name": "沙丘 (Dune)",
        "description": "炭灰 + 沙色，艺术/设计风",
        "ink": "#1f1a14",
        "ink_rgb": "31,26,20",
        "paper": "#f0e6d2",
        "paper_rgb": "240,230,210",
        "paper_tint": "#e3d7bf",
        "ink_tint": "#2d2620",
    },
}


def render_mermaid_svg(mermaid_code: str) -> Optional[str]:
    """Render mermaid diagram to SVG using mermaid-cli (mmdc)."""
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as mmd_f:
        mmd_f.write(mermaid_code)
        mmd_path = Path(mmd_f.name)

    svg_path = mmd_path.with_suffix('.svg')
    try:
        subprocess.run([
            "mmdc", "-i", str(mmd_path), "-o", str(svg_path),
            "-t", "default", "-b", "transparent"
        ], check=True, capture_output=True)
        svg_content = svg_path.read_text()
        return svg_content
    except subprocess.CalledProcessError:
        return None
    finally:
        mmd_path.unlink(missing_ok=True)
        svg_path.unlink(missing_ok=True)


def render_graphviz_svg(dot_code: str) -> Optional[str]:
    """Render graphviz dot to SVG."""
    try:
        result = subprocess.run(
            ["dot", "-Tsvg"],
            input=dot_code,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def extract_and_render_diagrams(md_text: str, inline_svg: bool = False) -> Tuple[str, dict]:
    """Extract mermaid/graphviz code blocks, render to SVG, replace in markdown."""
    svg_files = {}
    diagram_count = {"mermaid": 0, "dot": 0}

    def replace_diagram(match):
        lang = match.group(1).strip()
        code = match.group(2).strip()

        if lang == "mermaid":
            diagram_count["mermaid"] += 1
            svg_content = render_mermaid_svg(code)
            if svg_content:
                if inline_svg:
                    return f'\n<div class="diagram mermaid-diagram">{svg_content}</div>\n'
                else:
                    filename = f"diagram_mermaid_{diagram_count['mermaid']}.svg"
                    svg_files[filename] = svg_content
                    return f'\n<img src="{filename}" alt="Mermaid diagram" class="diagram mermaid-diagram">\n'

        elif lang in ("dot", "graphviz"):
            diagram_count["dot"] += 1
            svg_content = render_graphviz_svg(code)
            if svg_content:
                if inline_svg:
                    return f'\n<div class="diagram graphviz-diagram">{svg_content}</div>\n'
                else:
                    filename = f"diagram_graphviz_{diagram_count['dot']}.svg"
                    svg_files[filename] = svg_content
                    return f'\n<img src="{filename}" alt="Graphviz diagram" class="diagram graphviz-diagram">\n'

        return match.group(0)

    pattern = r'```(mermaid|dot|graphviz)\n(.*?)```'
    modified_md = re.sub(pattern, replace_diagram, md_text, flags=re.DOTALL)

    return modified_md, svg_files


def get_enhanced_css(theme_name: str = "monocle", enable_toc: bool = True) -> str:
    """Generate enhanced CSS with magazine theme + interactive features."""
    theme = THEMES.get(theme_name, THEMES["monocle"])

    # Base CSS variables
    css_vars = f"""
    :root {{
        /* Theme colors */
        --ink: {theme['ink']};
        --ink-rgb: {theme['ink_rgb']};
        --paper: {theme['paper']};
        --paper-rgb: {theme['paper_rgb']};
        --paper-tint: {theme['paper_tint']};
        --ink-tint: {theme['ink_tint']};

        /* Typography */
        --font-serif: "Noto Serif SC", "Playfair Display", Georgia, serif;
        --font-sans: "Noto Sans SC", Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;

        /* Layout */
        --content-width: 900px;
        --sidebar-width: 280px;
        --gap: 24px;
    }}
    """

    # Base styles
    base_css = """
    * { box-sizing: border-box; margin: 0; padding: 0; }

    html {
        scroll-behavior: smooth;
        font-size: 16px;
    }

    body {
        font-family: var(--font-sans);
        line-height: 1.7;
        color: var(--ink);
        background: var(--paper);
        padding: 0;
        overflow-x: hidden;
    }

    /* Reading progress bar */
    .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg,
            rgba(var(--ink-rgb), 0.3),
            rgba(var(--ink-rgb), 0.6));
        z-index: 1000;
        transition: width 0.1s ease-out;
    }

    /* Main layout */
    .container {
        display: flex;
        max-width: calc(var(--content-width) + var(--sidebar-width) + var(--gap) * 2);
        margin: 0 auto;
        padding: 40px 20px;
        gap: var(--gap);
    }

    /* Sidebar TOC */
    .toc-sidebar {
        position: sticky;
        top: 60px;
        width: var(--sidebar-width);
        height: fit-content;
        max-height: calc(100vh - 120px);
        overflow-y: auto;
        padding: 20px;
        background: rgba(var(--paper-tint-rgb, 232, 229, 222), 0.5);
        border-radius: 8px;
        font-size: 14px;
        display: """ + ("block" if enable_toc else "none") + """;
    }

    .toc-sidebar::-webkit-scrollbar {
        width: 4px;
    }

    .toc-sidebar::-webkit-scrollbar-thumb {
        background: rgba(var(--ink-rgb), 0.2);
        border-radius: 2px;
    }

    .toc-sidebar h3 {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: rgba(var(--ink-rgb), 0.5);
        margin-bottom: 12px;
    }

    .toc-sidebar ul {
        list-style: none;
    }

    .toc-sidebar li {
        margin: 8px 0;
    }

    .toc-sidebar a {
        color: rgba(var(--ink-rgb), 0.7);
        text-decoration: none;
        transition: color 0.2s;
        display: block;
    }

    .toc-sidebar a:hover {
        color: var(--ink);
    }

    .toc-sidebar a.active {
        color: var(--ink);
        font-weight: 500;
    }

    /* Main content */
    .content {
        flex: 1;
        min-width: 0;
        max-width: var(--content-width);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-serif);
        font-weight: 600;
        line-height: 1.3;
        margin-top: 2em;
        margin-bottom: 0.8em;
        color: var(--ink);
    }

    h1 {
        font-size: 2.5em;
        border-bottom: 2px solid rgba(var(--ink-rgb), 0.15);
        padding-bottom: 0.4em;
        margin-top: 0;
    }

    h2 {
        font-size: 2em;
        border-bottom: 1px solid rgba(var(--ink-rgb), 0.1);
        padding-bottom: 0.3em;
    }

    h3 { font-size: 1.5em; }
    h4 { font-size: 1.25em; }

    p {
        margin: 1.2em 0;
        text-align: justify;
    }

    /* Links */
    a {
        color: rgba(var(--ink-rgb), 0.8);
        text-decoration: underline;
        text-decoration-color: rgba(var(--ink-rgb), 0.3);
        text-underline-offset: 2px;
        transition: all 0.2s;
    }

    a:hover {
        color: var(--ink);
        text-decoration-color: rgba(var(--ink-rgb), 0.6);
    }

    /* Code blocks */
    code {
        font-family: var(--font-mono);
        font-size: 0.9em;
        background: var(--paper-tint);
        padding: 0.2em 0.5em;
        border-radius: 4px;
        color: var(--ink);
    }

    pre {
        position: relative;
        background: var(--paper-tint);
        padding: 20px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 1.5em 0;
        border: 1px solid rgba(var(--ink-rgb), 0.1);
    }

    pre code {
        background: none;
        padding: 0;
        font-size: 0.95em;
    }

    /* Copy button */
    .code-block-wrapper {
        position: relative;
    }

    .copy-button {
        position: absolute;
        top: 12px;
        right: 12px;
        padding: 6px 12px;
        font-size: 12px;
        font-family: var(--font-sans);
        background: rgba(var(--paper-rgb), 0.9);
        border: 1px solid rgba(var(--ink-rgb), 0.2);
        border-radius: 4px;
        color: var(--ink);
        cursor: pointer;
        transition: all 0.2s;
        opacity: 0;
    }

    .code-block-wrapper:hover .copy-button {
        opacity: 1;
    }

    .copy-button:hover {
        background: var(--paper);
        border-color: rgba(var(--ink-rgb), 0.4);
    }

    .copy-button.copied {
        background: var(--ink);
        color: var(--paper);
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5em 0;
        font-size: 0.95em;
    }

    th, td {
        padding: 12px 16px;
        text-align: left;
        border: 1px solid rgba(var(--ink-rgb), 0.15);
    }

    th {
        background: var(--paper-tint);
        font-weight: 600;
        font-family: var(--font-sans);
    }

    tr:nth-child(even) {
        background: rgba(var(--paper-tint-rgb, 232, 229, 222), 0.3);
    }

    /* Blockquotes */
    blockquote {
        border-left: 4px solid rgba(var(--ink-rgb), 0.3);
        padding-left: 20px;
        margin: 1.5em 0;
        color: rgba(var(--ink-rgb), 0.8);
        font-style: italic;
    }

    /* Lists */
    ul, ol {
        margin: 1em 0;
        padding-left: 2em;
    }

    li {
        margin: 0.5em 0;
    }

    /* Diagrams */
    .diagram {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 2em auto;
        padding: 20px;
        background: rgba(var(--paper-tint-rgb, 232, 229, 222), 0.3);
        border-radius: 8px;
    }

    .diagram svg {
        max-width: 100%;
        height: auto;
    }

    /* Print styles */
    @media print {
        .reading-progress,
        .toc-sidebar,
        .copy-button {
            display: none !important;
        }

        .container {
            display: block;
            max-width: 100%;
        }

        body {
            background: white;
            color: black;
        }

        pre {
            page-break-inside: avoid;
        }
    }

    /* Mobile responsive */
    @media (max-width: 1200px) {
        .toc-sidebar {
            display: none;
        }

        .container {
            padding: 20px 16px;
        }

        h1 { font-size: 2em; }
        h2 { font-size: 1.6em; }
    }
    """

    # Pygments syntax highlighting
    if HtmlFormatter:
        base_css += "\n" + HtmlFormatter(style='default').get_style_defs('.codehilite')

    return css_vars + base_css


def get_interactive_js(enable_toc: bool = True) -> str:
    """JavaScript for interactive features."""
    return f"""
    // Reading progress bar
    window.addEventListener('scroll', () => {{
        const winHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollPercent = (scrollTop / (docHeight - winHeight)) * 100;
        document.querySelector('.reading-progress').style.width = scrollPercent + '%';
    }});

    // Copy code buttons
    document.querySelectorAll('pre').forEach(pre => {{
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        wrapper.appendChild(button);

        button.addEventListener('click', async () => {{
            const code = pre.querySelector('code').textContent;
            await navigator.clipboard.writeText(code);
            button.textContent = 'Copied!';
            button.classList.add('copied');
            setTimeout(() => {{
                button.textContent = 'Copy';
                button.classList.remove('copied');
            }}, 2000);
        }});
    }});

    {'// TOC active state tracking' if enable_toc else ''}
    {'''
    const headings = document.querySelectorAll('h1, h2, h3, h4');
    const tocLinks = document.querySelectorAll('.toc-sidebar a');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                tocLinks.forEach(link => link.classList.remove('active'));
                const activeLink = document.querySelector(`.toc-sidebar a[href="#${id}"]`);
                if (activeLink) activeLink.classList.add('active');
            }
        });
    }, { rootMargin: '-20% 0px -80% 0px' });

    headings.forEach(h => observer.observe(h));
    ''' if enable_toc else ''}
    """


def render_markdown_to_html(
    md_text: str,
    theme: str = "monocle",
    inline_svg: bool = False,
    enable_toc: bool = True
) -> Tuple[str, dict]:
    """Render markdown to enhanced HTML."""
    # Extract and render diagrams
    md_text, svg_files = extract_and_render_diagrams(md_text, inline_svg)

    # Configure markdown extensions
    extensions = [
        'fenced_code',
        'tables',
        'toc',
        'nl2br',
        'sane_lists',
    ]

    if HtmlFormatter:
        extensions.append('codehilite')

    # Render markdown
    md = markdown.Markdown(extensions=extensions)
    body_html = md.convert(md_text)

    # Extract TOC
    toc_html = md.toc if hasattr(md, 'toc') else ""

    # Build HTML
    theme_obj = THEMES.get(theme, THEMES["monocle"])
    css = get_enhanced_css(theme, enable_toc)
    js = get_interactive_js(enable_toc)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Enhanced Markdown Document">
    <title>Markdown Document</title>
    <style>{css}</style>
</head>
<body>
    <div class="reading-progress"></div>

    <div class="container">
        {"" if not enable_toc else f'''
        <aside class="toc-sidebar">
            <h3>目录</h3>
            {toc_html if toc_html else '<p>暂无目录</p>'}
        </aside>
        '''}

        <main class="content">
            {body_html}
        </main>
    </div>

    <script>{js}</script>
</body>
</html>
"""

    return html, svg_files


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Markdown Renderer with Magazine Themes"
    )
    parser.add_argument("input", nargs='?', help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output HTML file")
    parser.add_argument("--theme",
                       choices=list(THEMES.keys()),
                       default="monocle",
                       help="Color theme (default: monocle)")
    parser.add_argument("--inline-svg", action="store_true",
                       help="Inline SVG diagrams")
    parser.add_argument("--no-toc", action="store_true",
                       help="Disable sidebar TOC")
    parser.add_argument("--list-themes", action="store_true",
                       help="List available themes")

    args = parser.parse_args()

    if args.list_themes:
        print("Available themes:\n")
        for key, theme in THEMES.items():
            print(f"{key:10} — {theme['name']}")
            print(f"           {theme['description']}\n")
        return

    if not args.input:
        parser.error("input file is required (unless using --list-themes)")

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix('.html')

    # Read and render
    md_text = input_path.read_text(encoding='utf-8')
    html, svg_files = render_markdown_to_html(
        md_text,
        theme=args.theme,
        inline_svg=args.inline_svg,
        enable_toc=not args.no_toc
    )

    # Write output
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML: {output_path}")
    print(f"   Theme: {THEMES[args.theme]['name']}")

    # Write SVG files
    if svg_files:
        for filename, content in svg_files.items():
            svg_path = output_path.parent / filename
            svg_path.write_text(content, encoding='utf-8')
            print(f"✅ SVG:  {svg_path}")

    print(f"\n渲染完成: {len(svg_files)} 个图表")


if __name__ == "__main__":
    main()
