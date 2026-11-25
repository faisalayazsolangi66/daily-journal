#!/usr/bin/env python3
"""Append dated entries to a journal file."""
import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_FILE = Path.home() / ".local" / "share" / "daily-journal" / "journal.md"
ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})", re.MULTILINE)


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        print("Error: date must be YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Append dated entries to a journal file.")
    parser.add_argument("--file", default=str(DEFAULT_FILE),
                        help="Journal file (default: ~/.local/share/daily-journal/journal.md)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Append an entry")
    p_add.add_argument("text", help="Journal entry text")
    p_add.add_argument("--date", default=date.today().isoformat(),
                       help="Entry date, YYYY-MM-DD (default: today)")
    p_add.add_argument("--title", default=None, help="Optional entry title")

    p_show = sub.add_parser("show", help="Show entries")
    p_show.add_argument("--date", default=None, help="Only this date, YYYY-MM-DD")
    p_show.add_argument("--last", type=int, default=None,
                        help="Show only the last N entries")

    p_search = sub.add_parser("search", help="Search entries")
    p_search.add_argument("query", help="Text to search for (case-insensitive)")

    sub.add_parser("dates", help="List all dates with entries")
    args = parser.parse_args()
    path = Path(args.file).expanduser()

    if args.command == "add":
        day = parse_date(args.date)
        heading = f"## {day.isoformat()}"
        if args.title:
            heading += f" — {args.title}"
        stamp = datetime.now().strftime("%H:%M")
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        with open(path, "a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            if existing:
                f.write("\n")
            f.write(f"{heading}\n\n*{stamp}*\n\n{args.text}\n")
        print(f"Entry added for {day} in {path}")

    elif args.command in ("show", "search", "dates"):
        if not path.exists():
            print("No journal entries yet.")
            return
        text = path.read_text(encoding="utf-8")
        # Split into (date, block) entries.
        matches = list(ENTRY_RE.finditer(text))
        entries = []
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            entries.append((m.group(1), text[start:end].strip()))
        if not entries:
            print("No dated entries found in the journal.")
            return
        if args.command == "dates":
            for d, _ in entries:
                print(d)
            return
        if args.command == "show":
            if args.date:
                parse_date(args.date)
                entries = [e for e in entries if e[0] == args.date]
            if args.last:
                entries = entries[-args.last:]
            if not entries:
                print("No matching entries.")
                return
            for _, block in entries:
                print(block)
                print()
        else:  # search
            query = args.query.lower()
            hits = [b for _, b in entries if query in b.lower()]
            if not hits:
                print(f"No entries matching {args.query!r}.")
                return
            print(f"{len(hits)} match(es):")
            for block in hits:
                print(block)
                print()


if __name__ == "__main__":
    main()
