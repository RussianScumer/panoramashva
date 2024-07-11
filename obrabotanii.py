import cv2
from PIL import Image
import numpy as np
import os
from stitching import AffineStitcher

global_scale = 3


def crop_center_one_third_height(image, scale):
    height, width = image.shape[:2]
    one_third_height = height // scale

    top = one_third_height
    bottom = 2 * one_third_height
    left = 0
    right = width

    cropped_image = image[top:bottom, left:right]
    return cropped_image


folder_path = 'frames/VID_20240604_104030'

file_list = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
file_list = sorted(file_list, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
file_list = list(reversed(file_list))
print(file_list)
resize_percent = 50  # сжимание для уменьшения размера

photo_array = []
# photo_array = np.array(photo_array)
for file in file_list:
    file_path = os.path.join(folder_path, file)
    img = Image.open(file_path)
    img_array = np.array(img)
    width = int(img_array.shape[1] * resize_percent / 100)
    height = int(img_array.shape[0] * resize_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img_array, dim, interpolation=cv2.INTER_AREA)
    img_array = crop_center_one_third_height(img_array, global_scale)
    photo_array.append(img_array)

print(photo_array)
# Преобразование в массив NumPy
photo_array = np.array(photo_array)
# im_v = cv2.vconcat(photo_array)
photo_array = np.concatenate(photo_array, axis=0)
photo_array = cv2.cvtColor(photo_array, cv2.COLOR_BGR2RGB)
cv2.imwrite('12345.png', photo_array)
cv2.imshow('test', photo_array)
cv2.waitKey()
