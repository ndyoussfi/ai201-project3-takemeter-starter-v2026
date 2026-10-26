#!/usr/bin/env python3
"""
Turn saved r/LocalLLaMA listing pages into rows of labels.csv. ← MILESTONE 4

Reddit blocks scripts from its JSON feed, so the pages are saved by hand: open
a listing in your browser, e.g.

    https://www.reddit.com/r/LocalLLaMA/new.json?limit=100
    https://www.reddit.com/r/LocalLLaMA/top.json?t=week&limit=100

and save it as a .json file (outside the repo is fine). Then:

    python collect.py ~/Downloads/new_1.json ~/Downloads/top_week.json

Each kept post becomes one row: title + blank line + body as `text`, with
`label` and `note` left empty for you to fill in. Rows are appended to
labels.csv, and a post whose text is already in the file is not added twice.

Skipped, following the reading rules in my notes:
  - posts with no body text (link-only, image-only)
  - cross-posts from other subreddits
  - removed or deleted posts, and stickied mod posts

Flair and Reddit's page text (upvotes, "Go to comments") are never in the
listing's title or body, so nothing extra has to be stripped.

The script prints the listing's `after` value. Add `&after=<value>` to the same
URL to get the next page.
"""

import argparse
import csv
import html
import json
import sys
from pathlib import Path

OUT = Path("labels.csv")
COLUMNS = ["text", "label", "note"]


def posts_in(listing_path):
    """Yield each post's data dict from one saved listing page, plus its `after`."""
    listing = json.loads(Path(listing_path).read_text(encoding="utf-8"))
    data = listing["data"]
    return [child["data"] for child in data["children"]], data.get("after")


def skip_reason(post):
    """Why a post is left out, or None to keep it."""
    body = post.get("selftext", "").strip()
    if post.get("stickied"):
        return "stickied"
    if post.get("crosspost_parent"):
        return "cross-post"
    if body in ("[removed]", "[deleted]"):
        return "removed"
    if not body:
        return "no body text"
    return None


def post_text(post):
    """Title and body, with Reddit's HTML escapes (&amp; and so on) undone."""
    title = html.unescape(post["title"]).strip()
    body = html.unescape(post["selftext"]).strip()
    return f"{title}\n\n{body}"


def existing_texts():
    if not OUT.exists():
        return set()
    with OUT.open(newline="", encoding="utf-8") as f:
        return {row["text"] for row in csv.DictReader(f)}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("listings", nargs="+", help="saved .json listing pages")
    args = parser.parse_args()

    seen = existing_texts()
    new_rows, skipped = [], {}

    for path in args.listings:
        posts, after = posts_in(path)
        for post in posts:
            reason = skip_reason(post)
            if reason:
                skipped[reason] = skipped.get(reason, 0) + 1
                continue
            text = post_text(post)
            if text in seen:
                skipped["already in labels.csv"] = skipped.get("already in labels.csv", 0) + 1
                continue
            seen.add(text)
            new_rows.append({"text": text, "label": "", "note": ""})
        print(f"{path}: {len(posts)} posts, next page after={after}")

    write_header = not OUT.exists()
    with OUT.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)

    print(f"\nAdded {len(new_rows)} rows to {OUT} ({len(seen)} total).")
    for reason, count in sorted(skipped.items(), key=lambda kv: -kv[1]):
        print(f"  skipped {count:3d}  {reason}")


if __name__ == "__main__":
    sys.exit(main())
