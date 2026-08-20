"""CLI entry point using Click."""

import sys
from pathlib import Path

import click

from file_organizer.config import load_config
from file_organizer.organizer import organize
from file_organizer.scanner import scan_directory


@click.command()
@click.argument("directory", required=False, type=click.Path(exists=True, path_type=Path))
@click.option("--dry-run", is_flag=True, help="Preview changes without moving files")
@click.option("--config", type=click.Path(path_type=Path), help="Path to config JSON")
@click.option("--by-date", is_flag=True, help="Organize into YYYY/MM folders")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--undo", is_flag=True, help="Undo the last organize run")
def main(directory: Path | None, dry_run: bool, config: Path | None, by_date: bool, verbose: bool, undo: bool) -> None:
    """Organize files in DIRECTORY into categorized subfolders, or undo the last run."""
    if undo:
        from file_organizer.undo import undo as undo_run
        undo_run()
        return

    if not directory:
        click.echo("Error: DIRECTORY is required unless --undo is used.", err=True)
        sys.exit(1)

    cfg = load_config(config)
    if by_date:
        cfg["by_date"] = True
    if verbose:
        cfg["verbose"] = True

    files = scan_directory(directory)
    organize(directory, files, dry_run=dry_run, config=cfg)


if __name__ == "__main__":
    sys.exit(main())
