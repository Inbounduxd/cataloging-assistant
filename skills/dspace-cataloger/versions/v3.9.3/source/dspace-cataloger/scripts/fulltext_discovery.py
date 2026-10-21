#!/usr/bin/env python3
"""
Offline helper: discover probable full-text representations from an HTML file.

It does NOT download remote content. It is intended for pipeline components that
already fetched the landing page. Uses only the Python standard library.
"""
from __future__ import annotations
from html.parser import HTMLParser
from urllib.parse import urljoin
import argparse, json, re
from pathlib import Path

PDF_RE = re.compile(r"\bpdf\b", re.I)
XML_RE = re.compile(r"\b(xml|jats)\b", re.I)
HTML_RE = re.compile(r"\b(full\s*text|html)\b", re.I)
EPUB_RE = re.compile(r"\bepub\b", re.I)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._type = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        data = dict(attrs)
        self._href = data.get("href")
        self._type = data.get("type")
        self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append({
                "href": self._href,
                "type": self._type,
                "text": " ".join("".join(self._text).split())
            })
            self._href = None
            self._type = None
            self._text = []

def classify(link):
    s = " ".join([
        link.get("text") or "",
        link.get("type") or "",
        link.get("href") or ""
    ])
    if PDF_RE.search(s) or ".pdf" in s.lower():
        return "PDF"
    if XML_RE.search(s) or ".xml" in s.lower():
        return "XML"
    if EPUB_RE.search(s) or ".epub" in s.lower():
        return "EPUB"
    if HTML_RE.search(s):
        return "HTML"
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_file")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    html = Path(args.html_file).read_text(encoding="utf-8", errors="replace")
    p = LinkParser()
    p.feed(html)

    reps = []
    seen = set()
    for link in p.links:
        kind = classify(link)
        if not kind:
            continue
        url = urljoin(args.base_url, link["href"])
        key = (kind, url)
        if key in seen:
            continue
        seen.add(key)
        reps.append({
            "kind": kind,
            "url": url,
            "anchorText": link.get("text"),
            "status": "DISCOVERED"
        })

    out = {"sourceUrl": args.base_url, "representations": reps}
    txt = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(txt, encoding="utf-8")
    else:
        print(txt)

if __name__ == "__main__":
    main()
