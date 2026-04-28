#!/usr/bin/env python3
"""IA user-flow — emit a mermaid flowchart from a list of steps."""
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("--steps", required=True, help="comma-separated step labels")
    p.add_argument("--branches", default="", help="step:branch_label, e.g. 'pay:fail->pay'")
    p.add_argument("-o", "--output")
    a = p.parse_args()
    steps = [s.strip() for s in a.steps.split(",")]
    lines = [f"flowchart LR", f"  %% {a.name}"]
    for i in range(len(steps)-1):
        lines.append(f"  {steps[i]} --> {steps[i+1]}")
    for b in filter(None, a.branches.split(",")):
        s, rest = b.split(":", 1)
        label, target = rest.split("->")
        lines.append(f"  {s} -- {label} --> {target}")
    out = "\n".join(lines)
    if a.output: open(a.output, "w").write(out); print(f"✓ → {a.output}")
    else: print(out)

if __name__ == "__main__": main()
