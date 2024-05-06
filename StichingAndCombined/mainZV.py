import os
from CutImage import CutImageOnTwoparts
from StichImageVertical import combine_images_vertically
from StichingImages import shovStiching
from getimage import get_images
import cv2
import numpy as np

# Укажите путь к папке с изображениями
# пути
image_folder = r'C:\OSPanel\domains\TgBot\panoramashva\images6000'
#1панорама
panorama1Path = 'Panorama1Part.jpg'
#Объединение изображений.
top_image_path = 'first_part_Panorama.jpg'
bottom_image_path = 'Panorama1Part.jpg'
output_path = 'combined_panorama_vertical3.jpg'

#
## тут должна быть функция для преобразования видоса в картинки
#


files = os.listdir(image_folder)

i = 0
# while i < len(files):
#     images = []
#     for j in range(5):
#         if i < len(files):
#             image_path = os.path.join(image_folder, files[i])
#             image = cv2.imread(image_path)
#             images.append(image)
#             i += 1
#         else:
#             break

    # Проходим по файлам в папке и добавляем изображения в массив
for i in range(0, len(files), 5):
        images = []
        for j in range(5):
            if i + j < len(files):
                image_path = os.path.join(image_folder, files[i+j])
                image = cv2.imread(image_path)
                images.append(image)


    if images:
        shovStiching(images)
        CutImageOnTwoparts(panorama1Path)
        combine_images_vertically(top_image_path, bottom_image_path, output_path)
        print(f"Обработано {len(images)} изображений")
    else:
        print("Все изображения обработаны")
        break




