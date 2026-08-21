# file-organizer

CLI tool to organize files by type and date. Scans a folder, classifies files into categories (Images, Documents, Code, Audio, Video, Archives, Others), and moves them into corresponding subfolders.

## Features

- **Dry-run preview** — see planned moves before touching anything
- **Date-based organization** — optional `--by-date` mode nests files under `YYYY/MM`
- **Custom rules** — load category definitions from a JSON config via `--config`
- **Safety first**:
  - Skips macOS bundles (`.app`, `.framework`, `.bundle`, `.plugin`) and project directories (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.)
  - Auto-renames colliding files instead of overwriting
  - Warns when a single run would move more than 200 files
- **Undo** — `--undo` reverses the last organize run using `~/.file-organizer/last_run.json`

## Install

```bash
pip install -e .
```

## Usage

```bash
# Preview changes
file-organizer /path/to/messy/folder --dry-run

# Organize for real
file-organizer ~/Downloads

# Organize by modification date
file-organizer ~/Downloads --by-date

# Undo the last organize run
file-organizer --undo
```

## Configuration

Use `--config path/to/rules.json` to override default category rules. Example:

```json
{
  "categories": {
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".txt", ".md"]
  },
  "skip_dirs": [".git", "node_modules"],
  "by_date": false,
  "verbose": false
}
```

## Undo

Every non-dry-run move is logged to `~/.file-organizer/last_run.json`. Run:

```bash
file-organizer --undo
```

to move files back to their original locations. If the original path is already occupied, undo skips that file instead of overwriting. The log is cleared after a successful undo.

## Development

Requires Python 3.10+. Run tests with:

```bash
python3 -m pytest tests/ -v
```
