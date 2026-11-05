# The Freebie Audiobook Directory

**Legal free audiobooks, explained like a friend would.** An education-only
directory of where to actually listen free, published as a plain-English
markdown directory plus a static HTML index page.

Built in the same warm, plain-English voice as the whole Asdale Dynamics education
library: friendly, step by step, never condescending.

- **Who it's for:** anyone curious about free, legal listening — including
  absolute beginners, nurses on break, and folks who just bought their first
  smartphone.
- **What's inside:** always-free classics (LibriVox, Internet Archive, Loyal
  Books, Lit2Go, Open Culture), library apps (Libby and Hoopla, explained in
  friend terms), podcast-first fiction (Welcome to Night Vale, The Magnus
  Archives, Escape Pod), and honest free-trial verdicts (Audible, Spotify,
  Everand, Chirp) — each with a one-line review and what device it works on.

## Distinct from library-ebooks-comfort-guide

This repo is the **audio** half of the pair. `library-ebooks-comfort-guide`
covers **ebooks vs audio** and reading comfort generally; there is minimal
overlap. If you want both shelves, keep both tabs open.

## Repo map

| File | What it is |
|---|---|
| `directory.md` | The freebie directory (markdown), by category, with friend reviews |
| `index.html` | Static HTML index page; open directly in any browser |
| `data/sources.json` | Canonical source list (single source of truth) |
| `build.py` | Regenerates `index.html` from `data/sources.json` (stdlib only) |
| `scripts/verify_links.py` | Checks every source URL resolves |
| `STATUS.md` | Current build status, verification results, known gaps |

## How to run

Requirements: Python 3.8+ (standard library only, no installs).

```bash
# Regenerate the static page from the data file:
python3 build.py

# Verify every link in the data file resolves:
python3 scripts/verify_links.py

# View the page: just open index.html in any browser, or serve it locally:
python3 -m http.server 8000    # then visit http://localhost:8000
```

`verify_links.py` exits 0 only when every URL is reachable. A handful of sites
return 401/403/429 to bots (anti-bot protection, e.g. Chirp) — those are
reported as *reachable-but-bot-blocked* and count as passing, since they open
normally in a real browser.

## Education only

This project is for education; it is not medical, legal, or financial advice.
Links may move or change at any time. No accounts, tracking, or personal data
are involved in building or browsing it.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

More plain-English AI guides: [dylanasdale.github.io](https://dylanasdale.github.io).
