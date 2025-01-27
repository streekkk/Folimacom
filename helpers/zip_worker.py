import glob
import os
import zipfile
from pathlib import Path
import shutil


def unzip_file(img_path: Path) -> Path:
    try:
        with zipfile.ZipFile(img_path, 'r') as zip_file:
           zip_file.extractall(img_path.parent)
        return img_path.parent
    except FileNotFoundError:
        return img_path
    except PermissionError:
        return img_path


def remove_zip(zip_path: Path) -> None:
    try:
        zip_path.unlink()
    except FileNotFoundError:
        pass
    except PermissionError:
        pass


def zip_file(source_dir: Path) -> None:
    try:
        with zipfile.ZipFile(f'{source_dir}', 'w') as zip_file:
            for file in source_dir.parent.rglob('*'):
                if file != source_dir:
                    zip_file.write(file, file.relative_to(source_dir.parent))
        for file in glob.glob(f"{source_dir.parent}/**", recursive=True):
            if Path(file) != source_dir and Path(file) != source_dir.parent:
                if os.path.isfile(file):
                    Path(file).unlink()
                elif os.path.isdir(file):
                  shutil.rmtree(file)
    except PermissionError:
        pass