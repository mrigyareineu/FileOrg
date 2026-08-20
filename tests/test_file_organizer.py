"""Tests using pytest."""

from pathlib import Path

from file_organizer.config import load_config
from file_organizer.organizer import categorize, organize
from file_organizer.scanner import scan_directory
import file_organizer.undo as undo_mod


def test_categorize_images() -> None:
    assert categorize(Path("photo.jpg")) == "Images"
    assert categorize(Path("diagram.png")) == "Images"


def test_categorize_code() -> None:
    assert categorize(Path("main.py")) == "Code"
    assert categorize(Path("app.ts")) == "Code"


def test_categorize_others() -> None:
    assert categorize(Path("unknown.xyz")) == "Others"


def test_scan_directory(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "sub" / "b.py").write_text("b")
    files = scan_directory(tmp_path)
    assert len(files) == 2


def test_scan_directory_skips_app_bundle(tmp_path: Path) -> None:
    (tmp_path / "Visual Studio Code.app" / "Contents" / "MacOS").mkdir(parents=True)
    (tmp_path / "Visual Studio Code.app" / "Contents" / "MacOS" / "code").write_text("x")
    (tmp_path / "normal.txt").write_text("y")
    files = scan_directory(tmp_path)
    assert len(files) == 1
    assert files[0].name == "normal.txt"


def test_scan_directory_skips_framework_bundle_plugin(tmp_path: Path) -> None:
    (tmp_path / "Foo.framework" / "Versions" / "A").mkdir(parents=True)
    (tmp_path / "Foo.framework" / "Versions" / "A" / "foo").write_text("x")
    (tmp_path / "Bar.bundle" / "Contents").mkdir(parents=True)
    (tmp_path / "Bar.bundle" / "Contents" / "info").write_text("x")
    (tmp_path / "Baz.plugin" / "Contents").mkdir(parents=True)
    (tmp_path / "Baz.plugin" / "Contents" / "plugin").write_text("x")
    (tmp_path / "normal.txt").write_text("y")
    files = scan_directory(tmp_path)
    assert len(files) == 1
    assert files[0].name == "normal.txt"


def test_scan_directory_skips_project_markers(tmp_path: Path) -> None:
    (tmp_path / "my-app" / "src").mkdir(parents=True)
    (tmp_path / "my-app" / "package.json").write_text("{}")
    (tmp_path / "my-app" / "src" / "App.tsx").write_text("x")
    (tmp_path / "my-app" / "node_modules").mkdir()
    (tmp_path / "my-app" / "node_modules" / "lib.js").write_text("y")
    (tmp_path / "normal.txt").write_text("z")
    files = scan_directory(tmp_path)
    assert len(files) == 1
    assert files[0].name == "normal.txt"


def test_organize_collision_auto_rename(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("first")
    (tmp_path / "Documents").mkdir()
    (tmp_path / "Documents" / "a.txt").write_text("existing")
    files = [tmp_path / "a.txt"]
    organize(tmp_path, files, dry_run=False)
    assert (tmp_path / "Documents" / "a.txt").exists()
    assert (tmp_path / "Documents" / "a (1).txt").exists()
    assert (tmp_path / "a.txt").exists() is False


def test_organize_undo_cycle(tmp_path: Path, monkeypatch: Any) -> None:
    log_file = tmp_path / "last_run.json"
    monkeypatch.setattr(undo_mod, "LOG_FILE", log_file)

    (tmp_path / "a.txt").write_text("first")
    (tmp_path / "b.py").write_text("second")
    files = scan_directory(tmp_path)
    organize(tmp_path, files, dry_run=False)

    assert not (tmp_path / "a.txt").exists()
    assert not (tmp_path / "b.py").exists()
    assert (tmp_path / "Documents" / "a.txt").exists()
    assert (tmp_path / "Code" / "b.py").exists()

    undo_mod.undo(log_file=log_file)

    assert (tmp_path / "a.txt").exists()
    assert (tmp_path / "b.py").exists()
    assert not (tmp_path / "Documents" / "a.txt").exists()
    assert not (tmp_path / "Code" / "b.py").exists()
    assert not log_file.exists()


def test_undo_skips_when_original_exists(tmp_path: Path, monkeypatch: Any) -> None:
    log_file = tmp_path / "last_run.json"
    monkeypatch.setattr(undo_mod, "LOG_FILE", log_file)

    (tmp_path / "a.txt").write_text("first")
    files = [tmp_path / "a.txt"]
    organize(tmp_path, files, dry_run=False)

    (tmp_path / "a.txt").write_text("new")

    undo_mod.undo(log_file=log_file)

    assert (tmp_path / "a.txt").read_text() == "new"
    assert (tmp_path / "Documents" / "a.txt").exists()
    assert not log_file.exists()
