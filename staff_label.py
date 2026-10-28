#!/usr/bin/env python3
"""
Label the 30 staff posts under data/staff_taxonomy.md. ← UNIT 6, MILESTONE 3

    python staff_label.py

Shows each post from data/staff_posts.csv with no suggestion. Type a key and
press Enter:

    a  analysis      h  hot_take      r  reaction      q  save and quit

Writes my_staff_labels.csv (text, label) with each post's text copied exactly,
which is what agreement.py matches on. Saved after every answer, and it resumes
where you stopped.
"""

import csv
import os
import sys
from pathlib import Path

POSTS = Path("data/staff_posts.csv")
OUT = Path("my_staff_labels.csv")
KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction"}


def main():
    with POSTS.open(newline="", encoding="utf-8") as f:
        posts = list(csv.DictReader(f))
    done = {}
    if OUT.exists():
        with OUT.open(newline="", encoding="utf-8") as f:
            done = {row["text"]: row["label"] for row in csv.DictReader(f)}

    for n, post in enumerate(posts, 1):
        if post["text"] in done:
            continue
        os.system("clear")
        print(f"── staff post {n} of {len(posts)} ({post['id']}) " + "─" * 30)
        print(post["text"])
        print("─" * 60)
        while True:
            key = input("a analysis · h hot_take · r reaction · q quit > ").strip().lower()
            if key == "q" or key in KEYS:
                break
        if key == "q":
            break
        done[post["text"]] = KEYS[key]
        with OUT.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["text", "label"])
            for p in posts:
                if p["text"] in done:
                    writer.writerow([p["text"], done[p["text"]]])

    print(f"\n{len(done)} of {len(posts)} labelled in {OUT}.")


if __name__ == "__main__":
    sys.exit(main())
