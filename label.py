#!/usr/bin/env python3
"""
Label labels.csv one post at a time, in the terminal. ← MILESTONE 4

    python label.py cold        # 20 random unlabelled posts, no suggestions, note = cold
    python label.py review      # pre-labelled rows in random order, until 150 usable rows
    python label.py counts      # label counts against criterion 4 (65% cap, 15% floor)
    python label.py finalize    # move skipped rows to data/skipped.csv and
                                # never-reviewed rows to data/unreviewed.csv

At each post, type a key and press Enter:

    a  announcement      r  results      h  help      s  skip (reaction, guide, junk)
    Enter alone          keep the suggested label (review mode only)
    q                    save and quit

Add a ! to flag a hard case, e.g. `r!`. You'll be asked which other label it
could have been and why you chose this one; that goes in the note column.

Every answer is saved straight away, so you can quit and come back.
"""

import csv
import os
import random
import sys
from pathlib import Path

CSV = Path("labels.csv")
SKIPPED = Path("data/skipped.csv")
UNREVIEWED = Path("data/unreviewed.csv")
COLUMNS = ["text", "label", "note"]
KEYS = {"a": "announcement", "r": "results", "h": "help", "s": "skip"}
LABELS = ["announcement", "results", "help"]
COLD_COUNT = 20
TARGET = 150    # the brief's stop rule: label down to 150 if behind on time


def load(path=CSV):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(rows, path=CSV):
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, path)


def add_note(row, text):
    row["note"] = f"{row['note']}; {text}" if row["note"] else text


def ask(row, position, total, suggestion=None):
    """Show one post and return (label, hard_case_note), or None to quit."""
    os.system("clear")
    print(f"── post {position} of {total} " + "─" * 50)
    print(row["text"])
    print("─" * 66)
    if suggestion:
        print(f"suggested: {suggestion}   (Enter keeps it)")
    while True:
        answer = input("a announcement · r results · h help · s skip · ! hard · q quit > ").strip().lower()
        if answer == "q":
            return None
        if answer == "" and suggestion:
            answer = next(k for k, v in KEYS.items() if v == suggestion)
        hard = answer.endswith("!")
        key = answer.rstrip("!")
        if key in KEYS:
            break
        print("  type a, r, h or s (add ! for a hard case)")
    hard_note = ""
    if hard:
        other = input("  hard case — the other label it could be: ").strip()
        why = input("  why you chose this one: ").strip()
        hard_note = f"hard: {KEYS[key]} vs {other}; {why}"
    return KEYS[key], hard_note


def cold_done(rows):
    """Cold labels that count: a skipped post doesn't, so skips are replaced."""
    return sum("cold" in r["note"] and r["label"] in LABELS for r in rows)


def cold(rows):
    todo = [i for i, r in enumerate(rows) if not r["label"]]
    random.shuffle(todo)
    for i in todo:
        if cold_done(rows) >= COLD_COUNT:
            break
        result = ask(rows[i], cold_done(rows) + 1, COLD_COUNT)
        if result is None:
            break
        rows[i]["label"], hard_note = result
        add_note(rows[i], "cold")
        if hard_note:
            add_note(rows[i], hard_note)
        save(rows)
    print(f"\n{cold_done(rows)} of {COLD_COUNT} cold labels done.")


def reviewed(row):
    """Labelled by me: cold, or a pre-label I read and confirmed or corrected."""
    return any(tag in row["note"] for tag in ("cold", "checked", "corrected"))


def usable(rows):
    """Rows that will be trained on: reviewed, and not skipped."""
    return sum(reviewed(r) and r["label"] in LABELS for r in rows)


def review(rows):
    """
    Review pre-labels in random order until TARGET usable rows exist (the
    brief's stop rule). Posts suggested as skip are left out of the queue,
    since they can't add a usable row; whatever is never reviewed is set
    aside by `finalize`, not trained on.
    """
    todo = [i for i, r in enumerate(rows)
            if "pre-labelled" in r["note"] and not reviewed(r) and r["label"] != "skip"]
    random.shuffle(todo)
    for i in todo:
        if usable(rows) >= TARGET:
            break
        suggestion = rows[i]["label"]
        result = ask(rows[i], usable(rows) + 1, TARGET, suggestion=suggestion)
        if result is None:
            break
        label, hard_note = result
        rows[i]["label"] = label
        add_note(rows[i], "checked" if label == suggestion else f"corrected (was {suggestion})")
        if hard_note:
            add_note(rows[i], hard_note)
        save(rows)
    print(f"\n{usable(rows)} of {TARGET} usable rows reviewed.")


def counts(rows):
    kept = [r for r in rows if r["label"] in LABELS]
    print(f"{len(rows)} rows: {len(kept)} labelled, "
          f"{sum(r['label'] == 'skip' for r in rows)} skipped, "
          f"{sum(not r['label'] for r in rows)} unlabelled\n")
    for label in LABELS:
        n = sum(r["label"] == label for r in kept)
        share = n / len(kept) if kept else 0
        flag = "  ← above 65%" if share > 0.65 else "  ← below 15%" if share < 0.15 else ""
        print(f"  {label:<13} {n:4d}  {share:6.1%}{flag}")
    print(f"\n  cold {cold_done(rows)}, "
          f"hard cases {sum('hard:' in r['note'] for r in rows)}, "
          f"usable reviewed {usable(rows)} of {TARGET}")


def finalize(rows):
    """Keep only reviewed, usable rows. Skips and never-reviewed pre-labels move out."""
    if any(not r["label"] for r in rows):
        print("Some rows are still unlabelled. Label them first.")
        return 1
    unreviewed = [r for r in rows if not reviewed(r)]
    skipped = [r for r in rows if reviewed(r) and r["label"] == "skip"]
    kept = [r for r in rows if reviewed(r) and r["label"] != "skip"]
    if skipped:
        save(load(SKIPPED) + skipped, SKIPPED)
    if unreviewed:
        save(load(UNREVIEWED) + unreviewed, UNREVIEWED)
    save(kept)
    print(f"Moved {len(skipped)} skipped rows to {SKIPPED} and {len(unreviewed)} never-reviewed "
          f"rows to {UNREVIEWED}. labels.csv now has {len(kept)} rows.")


def main():
    modes = {"cold": cold, "review": review, "counts": counts, "finalize": finalize}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        print(__doc__)
        return 1
    return modes[sys.argv[1]](load())


if __name__ == "__main__":
    sys.exit(main())
