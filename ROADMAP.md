"""
Practice Roadmap
----------------

Phase 1 — Make it run
1. pip install -e .
2. Run: file-organizer /path/to/messy/folder --dry-run
3. Verify it scans, categorizes, and prints planned moves.

Phase 2 — Add features
- [ ] Replace print() with rich.console.Console for colored output
- [ ] Add a progress bar (rich.progress) for large directories
- [ ] Support --by-date to nest folders under YYYY/MM
- [ ] Add --config to load category rules from a JSON file
- [ ] Add --undo feature (log moves to a file, reverse them)

Phase 3 — Polish
- [ ] Add logging module usage (log to file + console)
- [ ] Handle duplicate filenames (auto-rename with suffix)
- [ ] Add tests for organizer with pytest and tmp_path
- [ ] Add a --watch mode using watchdog or polling

Phase 4 — Ship it
- [ ] Add a README with install + usage
- [ ] Add a requirements-dev.txt for pytest, rich, click
- [ ] Add a GitHub Actions CI workflow (lint + test)

Tips:
- Work in small commits: git add -A && git commit -m "add scanner"
- Test with a temp folder first: mkdir /tmp/messy && touch /tmp/messy/{a.jpg,b.py,c.pdf}
- Read existing files in src/file_organizer/ before editing
"""
