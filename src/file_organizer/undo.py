"""Undo support for file-organizer."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


LOG_DIR = Path.home() / ".file-organizer"
LOG_FILE = LOG_DIR / "last_run.json"


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_move(original: Path, moved: Path, log_file: Path | None = None) -> None:
    """Append a move record to the undo log."""
    if log_file is None:
        log_file = LOG_FILE
    _ensure_log_dir()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "original": str(original),
        "moved": str(moved),
    }
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_log(log_file: Path | None = None) -> list[dict[str, Any]]:
    """Read all move records from the undo log."""
    if log_file is None:
        log_file = LOG_FILE
    if not log_file.exists():
        return []
    entries: list[dict[str, Any]] = []
    with log_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def clear_log(log_file: Path | None = None) -> None:
    """Remove the undo log file."""
    if log_file is None:
        log_file = LOG_FILE
    if log_file.exists():
        log_file.unlink()


def undo(log_file: Path | None = None) -> None:
    """Reverse all moves recorded in the undo log."""
    if log_file is None:
        log_file = LOG_FILE
    entries = read_log(log_file)
    if not entries:
        print("Nothing to undo.")
        return

    print(f"Undoing {len(entries)} moves...")
    restored = 0
    skipped = 0

    for entry in reversed(entries):
        original = Path(entry["original"])
        moved = Path(entry["moved"])

        if not moved.exists():
            print(f"SKIP: source no longer exists: {moved}")
            skipped += 1
            continue

        if original.exists():
            print(f"SKIP: original path already exists: {original}")
            skipped += 1
            continue

        moved.rename(original)
        print(f"Restored: {moved} -> {original}")
        restored += 1

    clear_log(log_file)
    print(f"Done. Restored {restored} files, skipped {skipped}.")
