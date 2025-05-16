from pathlib import Path
from random import randint


def create_folder(path: Path) -> Path:
    new_path = ""
    try:
        folder_name = path.name
        folder_name = str.split(folder_name, sep='.')[0]
        new_path = Path(f"{path.parent}/{folder_name}")
        new_path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        folder_name = randint(10000000, 99999999)
        new_path = Path(f"{path.parent}/{folder_name}")
        new_path.mkdir(parents=True, exist_ok=False)
    finally:
        return new_path
