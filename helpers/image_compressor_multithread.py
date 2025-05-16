from concurrent.futures import ThreadPoolExecutor
from helpers.image_compressor import compress_image


def compress_images_multithread(images_list: list) -> None:
    try:
        with ThreadPoolExecutor() as executor:
            executor.map(compress_image, images_list)
    except Exception as e:
        print(f"Ошибка при сжатии изображений: {e}")