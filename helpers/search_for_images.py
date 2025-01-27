import glob
from pathlib import Path


def search_for_images(img_path: Path) -> list[str]:
    jpg_path = f"{img_path}/**/*.jpg"
    images_list = glob.glob(jpg_path, recursive=True)
    return images_list
