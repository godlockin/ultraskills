#!/usr/bin/env python3
"""
md_render.py - Markdown → HTML + SVG renderer

Features:
- GitHub-flavored markdown → HTML
- Mermaid diagrams → SVG
- Graphviz (dot) → SVG
- Syntax highlighting (pygments)
- Standalone HTML output

Usage:
  python3 md_render.py input.md                    # Output to input.html
  python3 md_render.py input.md -o output.html     # Custom output
  python3 md_render.py input.md --inline-svg       # Inline SVG (no external files)
  python3 md_render.py input.md --theme dark       # Dark theme
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc, codehilite
except ImportError:
    print("Error: markdown not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)

try:
    from pygments.formatters import HtmlFormatter
except ImportError:
    print("Warning: pygments not installed. Syntax highlighting disabled.", file=sys.stderr)
    HtmlFormatter = None


def render_mermaid_svg(mermaid_code: str) -> Optional[str]:
    """Render mermaid diagram to SVG using mermaid-cli (mmdc)."""
    try:
        # Check if mmdc available
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


def extract_and_render_diagrams(md_text: str, inline_svg: bool = False) -> tuple[str, dict]:
    """Extract mermaid/graphviz code blocks, render to SVG, replace in markdown.

    Returns:
        (modified_md, svg_files) where svg_files = {filename: svg_content}
    """
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
                    return f'\n<div class="diagram">{svg_content}</div>\n'
                else:
                    filename = f"diagram_mermaid_{diagram_count['mermaid']}.svg"
                    svg_files[filename] = svg_content
                    return f'\n<img src="{filename}" alt="Mermaid diagram" class="diagram">\n'

        elif lang in ("dot", "graphviz"):
            diagram_count["dot"] += 1
            svg_content = render_graphviz_svg(code)
            if svg_content:
                if inline_svg:
                    return f'\n<div class="diagram">{svg_content}</div>\n'
                else:
                    filename = f"diagram_graphviz_{diagram_count['dot']}.svg"
                    svg_files[filename] = svg_content
                    return f'\n<img src="{filename}" alt="Graphviz diagram" class="diagram">\n'

        # Fallback: return original code block
        return match.group(0)

    # Match ```mermaid, ```dot, ```graphviz blocks
    pattern = r'```(mermaid|dot|graphviz)\n(.*?)```'
    modified_md = re.sub(pattern, replace_diagram, md_text, flags=re.DOTALL)

    return modified_md, svg_files


def get_css_theme(theme: str = "light") -> str:
    """Return CSS for the HTML output."""
    if theme == "dark":
        bg, fg, code_bg, border = "#1e1e1e", "#d4d4d4", "#2d2d2d", "#444"
    else:
        bg, fg, code_bg, border = "#ffffff", "#24292e", "#f6f8fa", "#e1e4e8"

    css = f"""
    * {{ box-sizing: border-box; }}
    body {{
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: {fg};
        background: {bg};
    }}
    h1, h2, h3, h4, h5, h6 {{
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
    }}
    h1 {{ border-bottom: 1px solid {border}; padding-bottom: 0.3em; }}
    h2 {{ border-bottom: 1px solid {border}; padding-bottom: 0.3em; }}
    code {{
        background: {code_bg};
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 85%;
    }}
    pre {{
        background: {code_bg};
        padding: 16px;
        overflow: auto;
        border-radius: 6px;
        line-height: 1.45;
    }}
    pre code {{
        background: transparent;
        padding: 0;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0;
    }}
    table th, table td {{
        border: 1px solid {border};
        padding: 6px 13px;
    }}
    table th {{
        background: {code_bg};
        font-weight: 600;
    }}
    blockquote {{
        border-left: 4px solid {border};
        padding-left: 16px;
        margin: 0;
        color: #6a737d;
    }}
    img, .diagram {{
        max-width: 100%;
        height: auto;
        display: block;
        margin: 16px 0;
    }}
    .diagram svg {{
        max-width: 100%;
        height: auto;
    }}
    a {{
        color: #0366d6;
        text-decoration: none;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    """

    # Add pygments syntax highlighting CSS if available
    if HtmlFormatter:
        css += "\n" + HtmlFormatter(style='github-dark' if theme == 'dark' else 'default').get_style_defs('.codehilite')

    return css


def render_markdown_to_html(
    md_text: str,
    theme: str = "light",
    inline_svg: bool = False
) -> tuple[str, dict]:
    """Render markdown to HTML with diagrams.

    Returns:
        (html_content, svg_files)
    """
    # Extract and render diagrams first
    md_text, svg_files = extract_and_render_diagrams(md_text, inline_svg)

    # Configure markdown extensions
    extensions = [
        'fenced_code',
        'tables',
        'toc',
        'nl2br',  # Newline to <br>
        'sane_lists',
    ]

    if HtmlFormatter:
        extensions.append('codehilite')

    # Render markdown to HTML
    md = markdown.Markdown(extensions=extensions)
    body_html = md.convert(md_text)

    # Build full HTML document
    css = get_css_theme(theme)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rendered Markdown</title>
    <style>
{css}
    </style>
</head>
<body>
{body_html}
</body>
</html>
"""

    return html, svg_files


def main():
    parser = argparse.ArgumentParser(
        description="Render Markdown to HTML with SVG diagram support"
    )
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output HTML file (default: input.html)")
    parser.add_argument("--inline-svg", action="store_true",
                       help="Inline SVG diagrams instead of external files")
    parser.add_argument("--theme", choices=["light", "dark"], default="light",
                       help="Color theme (default: light)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix('.html')

    # Read markdown
    md_text = input_path.read_text(encoding='utf-8')

    # Render
    html, svg_files = render_markdown_to_html(
        md_text,
        theme=args.theme,
        inline_svg=args.inline_svg
    )

    # Write HTML
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML: {output_path}")

    # Write SVG files (if not inlined)
    if svg_files:
        for filename, content in svg_files.items():
            svg_path = output_path.parent / filename
            svg_path.write_text(content, encoding='utf-8')
            print(f"✅ SVG:  {svg_path}")

    print(f"\nRendered {len(svg_files)} diagrams")


if __name__ == "__main__":
    main()
