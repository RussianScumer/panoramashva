import os
from CutImage import CutImageOnTwoparts
from StichImageVertical2 import combine_images_vertically
from StichingImages import shovStiching
import cv2
import numpy as np

# Укажите путь к папке с изображениями
# пути
image_folder = r'C:\OSPanel\domains\TgBot\panoramashva\2'
#1панорама
panorama1Path = 'Panorama1Part.jpg'
#Объединение изображений.
top_image_path = 'first_part_Panorama.jpg'
bottom_image_path = 'Panorama1Part.jpg'
output_path = 'combined_panorama_vertical3.jpg'

#
## тут должна быть функция для преобразования видоса в картинки
#

path = r'C:\OSPanel\domains\TgBot\panoramashva\images6000\1916.jpg'
image1 = cv2.imread(path)
window_name = 'image'


files = os.listdir(image_folder)

i = 0
while i < len(files):
    images = []
    for j in range(10):
        if i < len(files):
            image_path = os.path.join(image_folder, files[i])
            image = cv2.imread(image_path)
            images.append(image)
            i += 1
            cv2.imshow(window_name,image1)
    shovStiching(images)
    CutImageOnTwoparts(panorama1Path)
    combine_images_vertically(top_image_path,bottom_image_path,output_path)

    images.clear()




