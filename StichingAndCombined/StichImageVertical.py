from PIL import Image
from stitching import AffineStitcher
import cv2
import os

stitcher = AffineStitcher(blend_width=92)
def combine_images_vertically(top_image_path, bottom_image_path, output_path):
    # Открываем изображения
    top_image = Image.open(top_image_path)
    bottom_image = Image.open(bottom_image_path)
    # Создаем новое пустое изображение с достаточным размером
    print('xui')
    combined_image = stitcher.stitch([top_image_path,bottom_image_path])

    # Сохраняем объединенное изображение

    cv2.imwrite(output_path, combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('done')

# Пример использования
# top_image_path = 'first_part_Panorama.jpg'
# bottom_image_path = 'Panorama1Part.jpg'
# output_path = 'combined_panorama_vertical3.jpg'
# combine_images_vertically(top_image_path, bottom_image_path, output_path)