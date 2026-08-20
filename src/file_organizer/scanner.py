"""Scan a directory and collect files to organize."""

from __future__ import annotations

import os
from pathlib import Path


BUNDLE_EXTS = (".app", ".framework", ".bundle", ".plugin")
PROJECT_MARKERS = frozenset(
    {"package.json", ".git", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod"}
)


def _is_project_dir(directory: Path) -> bool:
    return any((directory / marker).exists() for marker in PROJECT_MARKERS)


def scan_directory(base: Path, skip_dirs: set[str] | None = None) -> list[Path]:
    """Return a list of files under base, excluding skip_dirs, bundle directories, and project directories."""
    if skip_dirs is None:
        skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}

    files: list[Path] = []
    for root, dirs, filenames in os.walk(base, topdown=True):
        dirs[:] = [
            d
            for d in dirs
            if not d.endswith(BUNDLE_EXTS)
            and d not in skip_dirs
            and not _is_project_dir(Path(root) / d)
        ]
        for filename in filenames:
            files.append(Path(root) / filename)
    return files
