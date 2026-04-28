#!/usr/bin/env python3
"""IA sitemap — YAML site spec → sitemap.json + optional mermaid."""
import argparse, json, sys

def load_yaml(path):
    try:
        import yaml
    except ImportError:
        print("Need PyYAML: pip install pyyaml", file=sys.stderr); sys.exit(1)
    return yaml.safe_load(open(path))

def flatten(node, parent=None, out=None):
    out = out if out is not None else []
    for n in node.get("nav", []) if isinstance(node, dict) and "nav" in node else node:
        entry = {"label": n["label"], "path": n.get("path",""), "parent": parent}
        out.append(entry)
        if "children" in n:
            flatten(n["children"], n["label"], out)
    return out

def to_mermaid(spec):
    lines = ["graph TD"]
    title = spec.get("title", "Site")
    lines.append(f"  ROOT[{title}]")
    def walk(items, parent="ROOT"):
        for n in items:
            label = n["label"].replace(" ", "_")
            node_id = label
            lines.append(f"  {parent} --> {node_id}[\"{n['label']} {n.get('path','')}\"]")
            if "children" in n:
                walk(n["children"], node_id)
    walk(spec.get("nav", []))
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("yaml_file")
    p.add_argument("-o", "--output", default="sitemap.json")
    p.add_argument("--mermaid", action="store_true")
    args = p.parse_args()
    spec = load_yaml(args.yaml_file)
    flat = flatten(spec)
    json.dump({"title": spec.get("title"), "pages": flat}, open(args.output, "w"),
              ensure_ascii=False, indent=2)
    print(f"✓ {len(flat)} pages → {args.output}")
    if args.mermaid:
        mfile = args.output.rsplit(".",1)[0] + ".mmd"
        open(mfile, "w").write(to_mermaid(spec))
        print(f"✓ mermaid → {mfile}")

if __name__ == "__main__": main()
