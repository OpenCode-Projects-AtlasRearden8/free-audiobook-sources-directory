#!/usr/bin/env python3
"""Build the static HTML index page from data/sources.json.

Standard library only. Run:  python3 build.py
Output: index.html (static, no JavaScript required)
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sources.json"
OUT = ROOT / "index.html"

CATEGORY_TITLES = {
    "always-free": "Always Free",
    "library-app": "Library Apps (Libby & Hoopla)",
    "podcast-fiction": "Podcast-First Fiction",
    "trial": "Free Trials (Worth It or Skippable)",
}

CATEGORY_INTROS = {
    "always-free": "No card, no trial, no catch. Public-domain classics and volunteer-read books, yours for the clicking.",
    "library-app": "Your library card is the single best free-audiobook tool you already own. Here is how the two big apps split the work.",
    "podcast-fiction": "Audio dramas and short-fiction podcasts that are free the way podcasts are free: subscribe and they just show up.",
    "trial": "Trials are only free if you remember to cancel. Each one gets an honest friend verdict: worth it, or skippable.",
}

CSS = """
:root{--ink:#1f2937;--muted:#6b7280;--accent:#1d4ed8;--card:#fff;--bg:#f8fafc;--line:#e5e7eb}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
.wrap{max-width:880px;margin:0 auto;padding:2rem 1.25rem 4rem}
header h1{font-size:2rem;margin:.2rem 0}
header p{color:var(--muted);margin-top:0}
.disclaimer{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:.75rem 1rem;font-size:.9rem;margin:1.5rem 0}
section{margin-top:2.5rem}
section h2{font-size:1.35rem;border-bottom:2px solid var(--line);padding-bottom:.35rem}
section p.intro{color:var(--muted);margin-top:.25rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.25rem;margin:1rem 0}
.card h3{margin:0;font-size:1.1rem}
.card .meta{font-size:.85rem;color:var(--muted);margin:.35rem 0}
.card .device{font-size:.9rem;color:var(--muted);margin:.25rem 0}
.card .review{margin:.5rem 0 0}
.card .verdict{margin:.5rem 0 0;font-size:.9rem}
.badge{display:inline-block;font-size:.75rem;font-weight:600;border-radius:999px;padding:.15rem .6rem;vertical-align:middle}
.badge.free{background:#dcfce7;color:#166534}
.badge.library{background:#dbeafe;color:#1e40af}
.badge.podcast{background:#f3e8ff;color:#6b21a8}
.badge.trial{background:#ffe4e6;color:#9f1239}
.verdict-worth{color:#166534}
.verdict-skip{color:#9f1239}
footer{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem;color:var(--muted);font-size:.85rem}
a{color:var(--accent)}
"""


def verdict_html(verdict: str) -> str:
    low = verdict.lower()
    cls = "verdict-worth" if low.lstrip().startswith("worth") else "verdict-skip"
    return f'<p class="verdict {cls}"><strong>Friend verdict:</strong> {html.escape(verdict)}</p>'


def build() -> str:
    data = json.loads(DATA.read_text(encoding="utf-8"))

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(data['title'])}</title>",
        "<style>" + CSS + "</style>",
        "</head>",
        "<body><div class='wrap'>",
        "<header>",
        f"<h1>{html.escape(data['title'])}</h1>",
        f"<p>{html.escape(data['subtitle'])} &middot; an education project by Asdale Dynamics, LLC</p>",
        "</header>",
        '<div class="disclaimer"><strong>Education only.</strong> '
        "This is a plain-English directory of legal ways to listen free. It is not legal, medical, or financial advice, "
        "prices and catalog sizes change, and nothing here tracks you or costs a dime.</div>",
    ]

    by_cat: dict[str, list[dict]] = {}
    for s in data["sources"]:
        by_cat.setdefault(s["category"], []).append(s)

    for cat, header in CATEGORY_TITLES.items():
        parts.append(f'<section id="{cat}">')
        parts.append(f"<h2>{html.escape(header)}</h2>")
        parts.append(f"<p class='intro'>{html.escape(CATEGORY_INTROS[cat])}</p>")
        for s in by_cat.get(cat, []):
            badge = f'<span class="badge {cat.replace("-", "")}">{html.escape(CATEGORY_TITLES[cat])}</span>'
            card = [
                '<div class="card">',
                f"<h3><a href=\"{html.escape(s['url'], quote=True)}\">{html.escape(s['name'])}</a> &nbsp;{badge}</h3>",
                f"<p class='meta'>{html.escape(s['cost'])}</p>",
                f"<p class='device'><strong>Works on:</strong> {html.escape(s['device'])}</p>",
                f"<p class='review'>&ldquo;{html.escape(s['review'])}&rdquo;</p>",
            ]
            if s.get("verdict"):
                card.append(verdict_html(s["verdict"]))
            card.append("</div>")
            parts.extend(card)
        parts.append("</section>")

    parts.append("<footer>")
    parts.append(
        "<p>Last verified with automated link checks. If a link moved, it usually still works via the site&rsquo;s home page.</p>"
    )
    parts.append(
        "<p>Part of the Asdale Dynamics beginner-education library. "
        "More plain-English guides at <a href='https://dylanasdale.github.io'>dylanasdale.github.io</a>. "
        "Copyright (c) 2026 Asdale Dynamics, LLC &middot; MIT License</p>"
    )
    parts.append("</footer></div></body></html>")
    return "\n".join(parts)


def main() -> None:
    content = build()
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
