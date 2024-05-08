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
# def zapolnenieMassiva(i):
#     if i == 0:
#         images = []
#         images.clear()
#         for j in range(7):
#             if i < len(files):
#                 image_path = os.path.join(image_folder, files[i + j])
#                 images.append(image_path)
#                 return images
#             else:
#                 break
#     else:
#         images = []
#         images.clear()
#         for j in range(7):
#             if j == 0:
#                 g = -1
#             else:
#                 g = 0
#             if i < len(files):
#                 image_path = os.path.join(image_folder, files[i + j + g])
#                 images.append(image_path)
#                 return images
#             else:
#                 break


# def zapolnenieMassiva(i):
#     images = []
#     start_index = i
#     end_index = i + 7
#
#     if i == 0:
#         for j in range(start_index, end_index):
#             if j < len(files):
#                 image_path = os.path.join(image_folder, files[j])
#                 images.append(image_path)
#     else:
#         last_image = images[-1]  # Получаем последний элемент предыдущего массива
#         images = [last_image]  # Начинаем новый массив с последнего элемента предыдущего
#
#         for j in range(start_index + 1, end_index):
#             if j < len(files):
#                 image_path = os.path.join(image_folder, files[j])
#                 images.append(image_path)
#
#     return images
# def zapolnenieMassiva(i):
#     images.clear()
#     if i == 0:
#         for j in range(7):
#             if i + j < len(files):
#                 image_path = os.path.join(image_folder, files[i + j])
#                 images.append(image_path)
#         return images
#     else:
#         for j in range(7):
#             if i + j < len(files):
#                 image_path = os.path.join(image_folder, files[i + j])
#                 images.append(image_path)
#         images.insert(0, images.pop())
#         return images

def zapolnenieMassiva(i):
    images = []
    if i == 0:
        for j in range(7):
            if i + j < len(files):
                image_path = os.path.join(image_folder, files[i + j])
                images.append(image_path)
    else:
        images.append(os.path.join(image_folder, files[i - 1]))
        for j in range(6):
            if i + j < len(files):
                image_path = os.path.join(image_folder, files[i + j])
                images.append(image_path)
    return images

i = 0
while i < 9:
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




