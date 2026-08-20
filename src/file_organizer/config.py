"""Configuration loading and defaults."""

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_CONFIG: dict = {
    "categories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
        "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".rb", ".php"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    },
    "skip_dirs": [".git", "__pycache__", "node_modules", ".venv", "venv"],
    "by_date": False,
    "verbose": False,
}


def load_config(path: Path | None) -> dict:
    """Load config from JSON file or return defaults."""
    if path and path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    return DEFAULT_CONFIG.copy()
