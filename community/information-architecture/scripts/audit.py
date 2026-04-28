#!/usr/bin/env python3
"""IA content audit — crawl a site, list URLs + titles + word counts."""
import argparse, csv, sys, urllib.parse, html
from collections import deque

try:
    import urllib.request
    from html.parser import HTMLParser
except ImportError:
    sys.exit("stdlib only")

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self.in_title = False; self.body = []; self.links = []
        self.in_body = False
    def handle_starttag(self, tag, attrs):
        if tag == "title": self.in_title = True
        if tag == "body": self.in_body = True
        if tag == "a":
            d = dict(attrs); h = d.get("href","")
            if h: self.links.append(h)
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, d):
        if self.in_title: self.title += d
        if self.in_body: self.body.append(d)

def fetch(u, timeout=8):
    try:
        return urllib.request.urlopen(u, timeout=timeout).read().decode("utf-8","ignore")
    except Exception as e:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("-o", "--output", default="audit.csv")
    a = ap.parse_args()
    base = urllib.parse.urlparse(a.url)
    seen = set(); q = deque([(a.url, 0)]); rows = []
    while q and len(rows) < a.max:
        u, d = q.popleft()
        if u in seen or d > a.depth: continue
        seen.add(u)
        h = fetch(u)
        if not h: continue
        p = P();
        try: p.feed(h)
        except Exception: pass
        words = len("".join(p.body).split())
        rows.append({"url": u, "title": p.title.strip()[:120], "words": words, "links_out": len(p.links)})
        for l in p.links:
            full = urllib.parse.urljoin(u, l)
            pu = urllib.parse.urlparse(full)
            if pu.netloc == base.netloc and full not in seen:
                q.append((full, d+1))
    with open(a.output, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url","title","words","links_out"]); w.writeheader()
        w.writerows(rows)
    print(f"✓ {len(rows)} pages → {a.output}")

if __name__ == "__main__": main()
