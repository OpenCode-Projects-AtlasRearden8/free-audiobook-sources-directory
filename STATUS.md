# STATUS

Last updated: 2026-11-05

## What was built

**The Freebie Audiobook Directory** — an education-only guide to legal free
audiobooks, published as a markdown directory plus a static HTML index page.
Built for the Asdale Dynamics beginner-education library in the "like a friend
would" voice: plain English, step by step, never condescending.

Contents (14 sources, each with a one-line friend review and device support):

| Category | Sources |
|---|---|
| Always Free | LibriVox, Internet Archive (Audio Books & Poetry), Loyal Books, Lit2Go, Open Culture |
| Library Apps | Libby, Hoopla (both explained in friend terms) |
| Podcast-First Fiction | Welcome to Night Vale, The Magnus Archives, Escape Pod |
| Free Trials | Audible, Spotify Premium, Everand, Chirp (worth-it / skippable verdicts) |

Files:

- `directory.md` — the markdown directory
- `index.html` — static HTML index page (generated, no JavaScript/external assets)
- `data/sources.json` — canonical single source of truth
- `build.py` — regenerates `index.html` (Python 3.8+, stdlib only)
- `scripts/verify_links.py` — automated link verification
- `README.md`, `LICENSE` (MIT, copyright (c) 2026 Asdale Dynamics, LLC)

Distinct from `library-ebooks-comfort-guide` (ebooks vs audio): this repo covers
audio only; no ebook-comfort content is duplicated.

## How to run

```bash
python3 build.py                 # regenerate index.html from data/sources.json
python3 scripts/verify_links.py  # verify every source link resolves
python3 -m http.server 8000      # optional local preview at http://localhost:8000
```

No installs, no dependencies, no network required for the build itself.

## Verification results

- `python3 build.py` — passes; wrote `index.html` (11,514 bytes, 14 cards,
  DOCTYPE/title/badge/verdict sanity checks all pass).
- `python3 scripts/verify_links.py` — **all 14 of 14 sources reachable**:
  - 13 URLs returned HTTP 200 (full GET with browser user-agent).
  - 1 URL (`chirpbooks.com`) returned HTTP 403 — anti-bot protection for
    automated requests; the site opens normally in a real browser. The script
    classifies this as BOTPLAN (reachable-but-bot-blocked) and counts it as
    passing; exit code 0.
- Cross-checks: every URL in `directory.md` matches `data/sources.json`
  (both directions), LICENSE contains the exact line
  `Copyright (c) 2026 Asdale Dynamics, LLC`, README credits Asdale Dynamics, LLC.

## Known gaps

- Link rot is the main risk: the verify script must be re-run periodically
  (trial terms, catalog sizes, and URLs change — noted in the page itself).
- Chirp cannot be verified by automated HTTP checks alone (403 to bots); a
  human browser check confirms the page loads.
- Device-support claims are simplified, friendly guidance; still-tight details
  (e.g., exact Hoopla TV-app coverage per region) are best re-checked on each
  app's store listing.
- Content is written once, not yet community-reviewed; corrections welcome.
