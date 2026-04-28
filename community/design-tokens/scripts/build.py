#!/usr/bin/env python3
"""design-tokens build — DTCG sources → CSS / Tailwind / SCSS / JSON."""
import argparse, json, os, re, sys, glob

REF_RE = re.compile(r"\{([^}]+)\}")

def deep_merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k,v in b.items():
            out[k] = deep_merge(a.get(k), v) if k in a else v
        return out
    return b if b is not None else a

def flatten(d, prefix=""):
    """Walk DTCG tree → dict[dotted_name] = (value, type)."""
    out = {}
    if not isinstance(d, dict): return out
    if "$value" in d:
        return {prefix.rstrip("."): (d["$value"], d.get("$type","other"))}
    for k, v in d.items():
        if k.startswith("$"): continue
        out.update(flatten(v, f"{prefix}{k}."))
    return out

def resolve(flat):
    """Resolve {a.b.c} references."""
    def lookup(name, seen):
        if name in seen: raise ValueError(f"cycle at {name}")
        if name not in flat: return f"{{{name}}}"  # leave unresolved
        v, t = flat[name]
        if isinstance(v, str) and "{" in v:
            return REF_RE.sub(lambda m: lookup(m.group(1), seen|{name}), v)
        return v
    return {k: (lookup(k, set()), t) for k, (v,t) in flat.items()}

def to_css_var(name): return "--" + name.replace(".", "-")

def emit_css(flat, selector=":root"):
    lines = [f"{selector} {{"]
    for k, (v, t) in sorted(flat.items()):
        # rewrite {ref} → var(--ref)
        v = REF_RE.sub(lambda m: f"var({to_css_var(m.group(1))})", str(v))
        lines.append(f"  {to_css_var(k)}: {v};")
    lines.append("}")
    return "\n".join(lines)

def emit_scss(flat):
    lines = []
    for k, (v, t) in sorted(flat.items()):
        v = REF_RE.sub(lambda m: f"${m.group(1).replace('.','-')}", str(v))
        lines.append(f"${k.replace('.','-')}: {v};")
    return "\n".join(lines)

def emit_tailwind(flat):
    """Reshape into tailwind theme.extend nested object."""
    out = {}
    for k, (v, t) in flat.items():
        parts = k.split(".")
        # color.brand.primary → colors.brand.primary
        if t == "color": parts = ["colors"] + parts[1:] if parts[0]=="color" else parts
        elif t == "dimension" and parts[0] == "spacing": parts = ["spacing"] + parts[1:]
        elif t == "dimension" and parts[0] == "radius": parts = ["borderRadius"] + parts[1:]
        cur = out
        for p in parts[:-1]: cur = cur.setdefault(p, {})
        cur[parts[-1]] = v if not str(v).startswith("{") else f"var({to_css_var(REF_RE.search(v).group(1))})"
    return "module.exports = { theme: { extend: " + json.dumps(out, indent=2) + " } };\n"

def emit_json(flat):
    return json.dumps({k: {"value": v, "type": t} for k,(v,t) in flat.items()}, indent=2)

def load_files(token_dir, files):
    merged = {}
    for f in files:
        p = os.path.join(token_dir, f)
        merged = deep_merge(merged, json.load(open(p)))
    return merged

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("token_dir")
    ap.add_argument("-o", "--out", default="dist")
    ap.add_argument("--formats", default="css,json", help="css,scss,tailwind,json")
    ap.add_argument("--themes", default="", help="name=file1+file2,name2=file3")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    formats = args.formats.split(",")

    if args.themes:
        css_chunks = []
        for theme_spec in args.themes.split(","):
            name, files = theme_spec.split("=", 1)
            tree = load_files(args.token_dir, files.split("+"))
            flat = resolve(flatten(tree))
            sel = ":root" if name == "light" else f"[data-theme=\"{name}\"]"
            if name == "light": sel = f":root, [data-theme=\"{name}\"]"
            for fmt in formats:
                if fmt == "css": css_chunks.append(emit_css(flat, sel))
                else:
                    open(f"{args.out}/{name}.{fmt_ext(fmt)}","w").write(emit(fmt, flat))
        if "css" in formats:
            open(f"{args.out}/tokens.css","w").write("\n\n".join(css_chunks))
            print(f"✓ {args.out}/tokens.css ({len(css_chunks)} themes)")
    else:
        all_files = [os.path.basename(p) for p in sorted(glob.glob(f"{args.token_dir}/*.json"))]
        tree = load_files(args.token_dir, all_files)
        flat = resolve(flatten(tree))
        for fmt in formats:
            content = emit(fmt, flat)
            ext = fmt_ext(fmt)
            path = f"{args.out}/tokens.{ext}" if fmt != "tailwind" else f"{args.out}/tailwind.config.js"
            open(path, "w").write(content)
            print(f"✓ {path} ({len(flat)} tokens)")

def fmt_ext(f): return {"css":"css","scss":"scss","json":"json","tailwind":"js"}[f]
def emit(f, flat):
    return {"css":emit_css, "scss":emit_scss, "tailwind":emit_tailwind, "json":emit_json}[f](flat)

if __name__ == "__main__": main()
