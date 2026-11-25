# daily-journal

Append dated entries to a journal file.

Entries are appended as Markdown sections in
`~/.local/share/daily-journal/journal.md` by default; use `--file`
to choose a different location.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py [--file journal.md] add "Today I ..." [--date 2026-11-25] [--title "A good day"]
python3 main.py show [--date 2026-11-25] [--last 5]
python3 main.py search "keyword"
python3 main.py dates
```

## Example

```bash
python3 main.py --file /tmp/journal.md add "Shipped the first video today."
python3 main.py --file /tmp/journal.md show
```

Sample output:

```
Entry added for 2026-11-25 in /tmp/journal.md
## 2026-11-25

*10:15*

Shipped the first video today.
```

## License

MIT — see `LICENSE`.
