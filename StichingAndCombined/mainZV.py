import os
from CutImage import CutImageOnTwoparts
from StichImageVertical2 import combine_images_vertically
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

files = os.listdir(image_folder)
numOfImages = 3
#
## тут должна быть функция для преобразования видоса в картинки
#

def keep_last(images):
       return [images[-1]]

def zapolnenieMassiva(i,images):
    if images:
        images = keep_last(images)
    for j in range(numOfImages):
        if i + j < len(files):
            image_path = os.path.join(image_folder, files[i + j])
            images.append(image_path)
    return images

def main():
    i = 0
    images = []
    while i < len(files):
        images = zapolnenieMassiva(i,images)
        print((images))
        if images:
                shovStiching(images)
                time.sleep(2)
                print((i))
                if i > 0:
                    CutImageOnTwoparts(output_path)
                else:
                    CutImageOnTwoparts(panorama1Path)
                combine_images_vertically(top_image_path, bottom_image_path, output_path)

                i += numOfImages
        else:
                print("Все изображения обработаны")
                break

if __name__ == '__main__':
    main()



