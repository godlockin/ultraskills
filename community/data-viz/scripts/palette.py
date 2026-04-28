#!/usr/bin/env python3
"""data-viz palette — emit categorical/sequential/diverging palettes."""
import argparse, json

# Okabe-Ito (color-blind safe categorical)
OKABE_ITO = ["#000000","#E69F00","#56B4E9","#009E73","#F0E442",
             "#0072B2","#D55E00","#CC79A7"]

# viridis (sequential, color-blind safe)
VIRIDIS = ["#440154","#482878","#3e4989","#31688e","#26828e",
           "#1f9e89","#35b779","#6ece58","#b5de2b","#fde725"]

# RdBu (diverging)
RDBU = ["#67001f","#b2182b","#d6604d","#f4a582","#fddbc7",
        "#f7f7f7","#d1e5f0","#92c5de","#4393c3","#2166ac","#053061"]

def sample(arr, n):
    if n >= len(arr): return arr
    step = (len(arr)-1) / (n-1)
    return [arr[round(i*step)] for i in range(n)]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--type", choices=["categorical","sequential","diverging"], default="categorical")
    p.add_argument("--n", type=int, default=8)
    p.add_argument("--colorblind", action="store_true",
                   help="ensure color-blind safe (default for cat/seq)")
    args = p.parse_args()

    if args.type == "categorical":
        cols = OKABE_ITO[:args.n] if args.n <= len(OKABE_ITO) else OKABE_ITO * (args.n // len(OKABE_ITO) + 1)
        cols = cols[:args.n]
    elif args.type == "sequential":
        cols = sample(VIRIDIS, args.n)
    else:
        cols = sample(RDBU, args.n)

    print(json.dumps({"type": args.type, "n": args.n, "colors": cols}, indent=2))

if __name__ == "__main__":
    main()
