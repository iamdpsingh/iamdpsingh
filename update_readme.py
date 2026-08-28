#!/usr/bin/env python3
"""
Auto-updates README.md:
  1. Refreshes the "Last Updated" badge with the current month/year.
  2. Flips the availability status line between:
       - "available for internships now, full-time from June 2026"
       - "available full-time now"
     based on whether today's date has passed the FULL_TIME_FROM date below.

Runs via GitHub Actions on a schedule (see .github/workflows/update-readme.yml).
"""

import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

README_PATH = "README.md"
ASSETS_DIR = Path("assets")
GITHUB_USERNAME = "iamdpsingh"

# (local filename, source URL) pairs to refresh on every run.
# If a fetch fails, the previously cached file is left untouched so the
# README never shows a broken image.
STATS_SOURCES = {
    "stats.svg": (
        "https://github-stats-extended.vercel.app/api"
        f"?username={GITHUB_USERNAME}&show_icons=true&theme=tokyonight"
        "&hide_border=true&count_private=true"
    ),
    "top-langs.svg": (
        "https://github-stats-extended.vercel.app/api/top-langs/"
        f"?username={GITHUB_USERNAME}&layout=compact&theme=tokyonight&hide_border=true"
    ),
    "streak.svg": (
        "https://streak-stats.demolab.com/"
        f"?user={GITHUB_USERNAME}&theme=tokyonight&hide_border=true"
    ),
    "trophy.svg": (
        "https://github-profile-trophy.vercel.app/"
        f"?username={GITHUB_USERNAME}&theme=algolia&no-frame=true&no-bg=false"
        "&row=1&column=7&margin-w=8&margin-h=8"
    ),
}


def refresh_stats_assets() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    for filename, url in STATS_SOURCES.items():
        dest = ASSETS_DIR / filename
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            # Basic sanity check: make sure we actually got SVG content,
            # not an HTML error page from a paused/rate-limited service.
            if b"<svg" not in data[:2000]:
                raise ValueError("response did not look like an SVG")
            dest.write_bytes(data)
            print(f"  updated {dest} from {url}")
        except Exception as exc:  # noqa: BLE001 - keep the run going regardless
            if dest.exists():
                print(f"  fetch failed for {filename} ({exc}); keeping cached version")
            else:
                print(f"  fetch failed for {filename} ({exc}); no cached version exists yet")

# The month/year you become available full-time. Change this if your plans change.
FULL_TIME_FROM = date(2026, 6, 1)

TODAY = date.today()
MONTH_YEAR = TODAY.strftime("%B %Y")           # e.g. "August 2026"
MONTH_YEAR_BADGE = TODAY.strftime("%B%%20%Y")  # URL-encoded for shields.io badge text


def build_date_block() -> str:
    badge_url = (
        "https://img.shields.io/badge/Last%20Updated-"
        f"{MONTH_YEAR_BADGE}-2E9EF7?style=for-the-badge"
    )
    return (
        '<!--DATE_START-->\n'
        '<p align="center">\n'
        f'  <img src="{badge_url}" alt="Last Updated" />\n'
        '</p>\n'
        '<!--DATE_END-->'
    )


def build_status_block() -> str:
    if TODAY >= FULL_TIME_FROM:
        availability = "available full-time now"
    else:
        availability = (
            f"available for internships now, full-time from "
            f"{FULL_TIME_FROM.strftime('%B %Y')}"
        )
    line = (
        "- 🌍 **Open to remote Data QA / Data Analytics / Data Science / "
        f"Data Engineering roles** — {availability}"
    )
    return f"<!--STATUS_START-->\n{line}\n<!--STATUS_END-->"


def build_footer_status_block() -> str:
    if TODAY >= FULL_TIME_FROM:
        availability = "available full-time now"
    else:
        availability = (
            f"available for internships now, full-time from "
            f"{FULL_TIME_FROM.strftime('%B %Y')}"
        )
    line = (
        '<p align="center"><i>🌍 Open to remote Data Analytics / Data Science / '
        f"Data Engineering roles worldwide — {availability}. Let's connect!</i></p>"
    )
    return f"<!--FOOTER_STATUS_START-->\n{line}\n<!--FOOTER_STATUS_END-->"


def replace_block(content: str, start_marker: str, end_marker: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    if not pattern.search(content):
        raise ValueError(f"Markers {start_marker} / {end_marker} not found in README.md")
    return pattern.sub(new_block, content, count=1)


def main() -> None:
    print("Refreshing cached stats SVGs...")
    refresh_stats_assets()

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(content, "<!--DATE_START-->", "<!--DATE_END-->", build_date_block())
    content = replace_block(content, "<!--STATUS_START-->", "<!--STATUS_END-->", build_status_block())
    content = replace_block(
        content, "<!--FOOTER_STATUS_START-->", "<!--FOOTER_STATUS_END-->", build_footer_status_block()
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"README.md updated for {MONTH_YEAR}.")


if __name__ == "__main__":
    main()
