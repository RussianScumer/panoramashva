import os
import cv2

from flowvideo import flowvideo
from speed_calculator import find_tape_coordinates, calculate_speed
from utils import save_frames_from_vid_40sec
from PIL import Image
import numpy as np
from ClearDirectory import delete_files_in_folder

'''
Все необходимые переменные
'''

video_path = '4'  #название видео без .mp4
saved_img_name = '12345'  #название сохраннённого изображения
size_of_frames = 5  # то какую часть в последующем будем брать из видео
auto = True   #замер скорости изоленты, если True, замеряет скорость автоматически по СИНЕЙ изленте в видео
#если False, необходимо рассчиать videothresh вручную
videothresh = 235  # частота кадров, через которую берем их из видео из расчёта 30 кадров
# в секунду 30*время смены кадра% size_of_frames
framecount = -150  # задержка, чтобы пропустить остановку и т.п (-150  это простой камеры в кадрах 30*sec  )
#замер скорости
'''
Функция для обрезания нужной центральной части кадра
params: 
image - изображение
scale - int, 1/scale = та часть кадра которую хотим брать, в нашем случае 1/3 или 1/5 можно пробовать другие с этими 
значениямии - лучший результат
'''


def crop_center_one_fifth_height(image, scale):
    height, width = image.shape[:2]
    one_fifth_height = (height // scale)

    top = one_fifth_height
    bottom = 2 * one_fifth_height
    left = 0
    right = width

    cropped_image = image[top:bottom, left:right]
    return cropped_image


folder_path = 'frames/4'  # Замените на путь к нужной папке
delete_files_in_folder(folder_path)
imagelast = 0
vidcap = cv2.VideoCapture('videos/%s' % video_path + '.mp4')
success, image = vidcap.read()
what_flow = flowvideo(video_path + '.mp4')  #определение направления видео
count = 0
dim = (1920, 1080)
if auto:
    save_frames_from_vid_40sec('videos/%s' % video_path + '.mp4', 'save_auto_speed_count')
    videothresh = calculate_speed(find_tape_coordinates('save_auto_speed_count'), 100)
    videothresh = int((720 / videothresh) / (size_of_frames))
    videothresh = int(videothresh + videothresh * 0.05)
    print(videothresh)

image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

if not os.path.exists('frames/%s' % video_path):
    os.makedirs('frames/%s' % video_path)

cv2.imwrite("frames/%s/%d.jpg" % (video_path, count), crop_center_one_fifth_height(image, size_of_frames))
#сохранение кадров с оставлением нужной части, для последующей склейки
while success:
    success, image = vidcap.read()
    framecount += 1
    if image is not None:
        imagelast = image
    if framecount == videothresh:
        framecount = 0
    else:
        continue
    if image is not None:
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        if not what_flow:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("frames/%s/%d.jpg" % (video_path, count), crop_center_one_fifth_height(image, size_of_frames))
    print('Read a new frame: ', success)
    count += 1

imagelast = cv2.resize(imagelast, dim, interpolation=cv2.INTER_AREA)
count += 2
print(count + 2)

folder_path = "frames/%s" % video_path

file_list = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
file_list = sorted(file_list, key=lambda x: int(x.split('frame')[-1].split('.')[0]))
print(file_list)
resize_percent = 50  # сжимание для уменьшения размера

photo_array = []
# собираем все в один np array
for file in file_list:
    file_path = os.path.join(folder_path, file)
    img = Image.open(file_path)
    img_array = np.array(img)
    width = int(img_array.shape[1] * resize_percent / 100)
    height = int(img_array.shape[0] * resize_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img_array, dim, interpolation=cv2.INTER_AREA)
    photo_array.append(img_array)

print(photo_array)
photo_array = np.array(photo_array)
#склейка
photo_array = np.concatenate(photo_array, axis=0)
photo_array = cv2.cvtColor(photo_array, cv2.COLOR_BGR2RGB)

cv2.imwrite(saved_img_name + '.png', photo_array)
cv2.imshow('test', photo_array)
print("done")
cv2.waitKey()
