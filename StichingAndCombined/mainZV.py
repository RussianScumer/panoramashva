import os
from CutImage import CutImageOnTwoparts
from StichImageVertical import combine_images_vertically
from StichingImages import shovStiching

import cv2
import numpy as np
import time

# Укажите путь к папке с изображениями
# пути
image_folder = r'C:\OSPanel\domains\TgBot\panoramashva\images6002'
#1панорама
panorama1Path = 'Panorama1Part.png'
#Объединение изображений.
top_image_path = 'first_part_Panorama.png'
bottom_image_path = 'Panorama1Part.png'
output_path = 'combined_panorama_vertical3.png'

#
## тут должна быть функция для преобразования видоса в картинки
#
files = os.listdir(image_folder)


def keep_last(lst):
    return lst[-1]

def zapolnenieMassiva(i,images):
    if images:
        images = keep_last(images)
    for j in range(7):
        if i + j < len(files):
            image_path = os.path.join(image_folder, files[i + j])
            images.append(image_path)
    return images

i = 0
while i < len(files):
    images = []
    images = zapolnenieMassiva(i)
    print((images))
    if images:
            shovStiching(images)
            print((i))
            if i > 0:
                CutImageOnTwoparts(output_path)
            else:
                CutImageOnTwoparts(panorama1Path)
            combine_images_vertically(top_image_path, bottom_image_path, output_path)
            time.sleep(2)
            i += 7
    else:
            print("Все изображения обработаны")
            break




