from PIL import Image


def compress_image(img_path: str, quality=75) -> None:
    image = Image.open(img_path)
    image = image.convert('RGB')
    image = image.resize(image.size, Image.Resampling.LANCZOS)
    image.save(f"{img_path}", optimize=True, quality=quality)