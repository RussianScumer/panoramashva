import cv2
from PIL import Image
import numpy as np
import os

# Путь к папке с фотографиями
folder_path = 'Test'

# Получение списка имен файлов
file_list = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
file_list = sorted(file_list, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
print(file_list)
# Создание их массива NumPy
photo_array = []
for file in file_list:
    file_path = os.path.join(folder_path, file)
    img = Image.open(file_path)
    img_array = np.array(img)
    photo_array.append(img_array)

print(photo_array)
# Преобразование в массив NumPy
photo_array = np.array(photo_array)
photo_array = np.concatenate(photo_array, axis=0)

cv2.imwrite('test.jpg', photo_array)
cv2.imshow('test', photo_array)
cv2.waitKey()
