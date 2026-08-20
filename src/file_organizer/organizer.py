"""Organize files into categorized directories."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any

from file_organizer.undo import log_move


EXT_TO_CATEGORY: dict[str, str] = {
    ext: cat
    for cat, exts in {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
        "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".rb", ".php"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    }.items()
    for ext in exts
}


def categorize(file_path: Path) -> str:
    """Return category name for a file based on extension."""
    return EXT_TO_CATEGORY.get(file_path.suffix.lower(), "Others")


def date_path(file_path: Path) -> Path:
    """Return a relative date path like 2026/08."""
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return Path(str(mtime.year), f"{mtime.month:02d}")


def unique_path(target: Path) -> Path:
    """Return a unique path, appending a counter suffix if the target already exists."""
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize(
    base: Path,
    files: list[Path],
    dry_run: bool = True,
    config: dict[str, Any] | None = None,
) -> None:
    """Move files into category folders, optionally nested under date folders."""
    if config is None:
        config = {}

    if dry_run and len(files) > 200:
        print(
            f"WARNING: This would move {len(files)} files. "
            "This looks unusually large — are you sure this is the folder you meant?"
        )

    moved = 0
    skipped = 0

    for file_path in files:
        category = categorize(file_path)
        target_dir = base / category
        if config.get("by_date"):
            target_dir = target_dir / date_path(file_path)

        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / file_path.name

        if target == file_path:
            skipped += 1
            continue

        if target.exists():
            target = unique_path(target)

        if dry_run:
            print(f"[DRY RUN] {file_path} -> {target}")
        else:
            file_path.rename(target)
            log_move(file_path, target)
            print(f"Moved: {file_path} -> {target}")
        moved += 1

    print(f"Done. Would move {moved} files, skipped {skipped}.")
