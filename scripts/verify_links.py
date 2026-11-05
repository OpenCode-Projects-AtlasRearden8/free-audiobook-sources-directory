#!/usr/bin/env python3
"""Verify that every source URL evaluates as reachable.

Standard library only (urllib). Verdicts:
  OK       2xx/3xx response, or a redirect that resolves
  BOTPLAN  401/403/429 — site is anti-bot protected; human-reachable in a browser
  FAIL     anything else (connection error, 404, 5xx)

Run:  python3 scripts/verify_links.py   (exit code 0 only if no FAIL)
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "sources.json"
TIMEOUT = 20
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def check(url: str) -> tuple[str, int | None]:
    req = urllib.request.Request(
        url, method="GET", headers={"User-Agent": UA, "Accept": "*/*"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return "OK", resp.status
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429):
            return "BOTPLAN", e.code
        return "FAIL", e.code
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return "FAIL", None if isinstance(e, TimeoutError) else -1


def main() -> int:
    sources = json.loads(DATA.read_text(encoding="utf-8"))["sources"]
    failures = []
    botplans = []
    for s in sources:
        url = s["url"]
        verdict, code = check(url)
        name = s["name"]
        if verdict == "FAIL":
            failures.append((name, url, code))
        elif verdict == "BOTPLAN":
            botplans.append((name, url, code))
        print(f"[{verdict:<7}] {name}: {url} (status={code})")
    print()
    if botplans:
        print(f"reachable-but-bot-blocked ({len(botplans)}):")
        for name, url, code in botplans:
            print(f"  - {name}: {url} (HTTP {code}; opens fine in a normal browser)")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for name, url, code in failures:
            print(f"  - {name}: {url} (status={code})")
        return 1
    print(f"\nAll {len(sources)} sources reachable (incl. {len(botplans)} bot-blocked-but-human-reachable).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
