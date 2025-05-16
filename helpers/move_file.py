from pathlib import Path


def move_file(old_path: Path, new_path: Path) -> Path:
    file_name = old_path.name
    new_file_path = Path(old_path).rename(new_path / file_name)
    return new_file_path