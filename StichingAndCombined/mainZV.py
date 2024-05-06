import os
from CutImage import CutImageOnTwoparts
from StichImageVertical import combine_images_vertically
from StichingImages import shovStiching
from getimage import get_images
import cv2
import numpy as np
import time
# Укажите путь к папке с изображениями
# пути
image_folder = r'H:\panoramashva\panoramashva\Test'
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
while i < len(files):

    images = []
    images.clear()
    for j in range(7):
        if i < len(files):
            image_path = os.path.join(image_folder, files[i+j])
            images.append(image_path)
            print((images))

        else:
            break
    if images:
        shovStiching(images)

        print((i))
        if i > 0:
            CutImageOnTwoparts(output_path)
        else:
            CutImageOnTwoparts(panorama1Path)

        combine_images_vertically(top_image_path, bottom_image_path, output_path)

        print(f"Обработано {len(images)} изображений")

        # time.sleep(2)
        i += 7
    else:
        print("Все изображения обработаны")
        break




