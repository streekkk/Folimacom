from PIL import Image


def compress_image(img_path: str, quality=75) -> None:
    image = Image.open(img_path)
    image = image.resize(image.size)
    image.save(img_path, optimize=True, quality=quality)
