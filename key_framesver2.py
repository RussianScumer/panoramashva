import os

import cv2
from speed_calculator import find_tape_coordinates, calculate_speed
from utils import save_frames_from_vid_40sec

video_path = 'VID_20240604_104142'


def crop_center_one_third_height(image, scale):
    height, width = image.shape[:2]
    one_third_height = int(height // scale)

    top = one_third_height
    bottom = 2 * one_third_height
    left = 0
    right = width

    cropped_image = image[top:bottom, left:right]
    return cropped_image


auto = False
size_of_frames = 3  # то какую часть в последующем будем брать из видео
imagelast = 0
vidcap = cv2.VideoCapture('videos/%s' % video_path + '.mp4')
success, image = vidcap.read()
count = 0
dim = (1920, 1080)
videothresh = 60  # частота кадров, через которую берем их из видео из расчёта 30 кадров в секунду
framecount = 0  # задержка, чтобы пропустить остановку и т.п
# пока работает не очень верно на видео что есть, т.к. изолента движется с первой половины кадра из за чего возникают
# проблемы, требуется чтобы на видео была изолента/любой синий или другой объект который ОТЛИЧАЕТСЯ цветов от отражения
# на детали, или же света падающего на неё и все будет считаться нормально(посчитано)
if auto:
    save_frames_from_vid_40sec('videos/%s' % video_path + '.mp4', 'save_auto_speed_count')
    videothresh = calculate_speed(find_tape_coordinates('save_auto_speed_count'), 100)
    videothresh = int((1080 / videothresh) / (size_of_frames))
    print(videothresh)

image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

if not os.path.exists('frames/%s' % video_path):
    os.makedirs('frames/%s' % video_path)

cv2.imwrite("frames/%s/%d.jpg" % (video_path, count), crop_center_one_third_height(image, size_of_frames))
# images.append(image)
while success:
    # cv2.imwrite("test/frame%d.jpg" % count, image)
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
        # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("frames/%s/%d.jpg" % (video_path, count), crop_center_one_third_height(image, size_of_frames))
        # images.append(image)
    print('Read a new frame: ', success)
    count += 1
# print(imagelast)
imagelast = cv2.resize(imagelast, dim, interpolation=cv2.INTER_AREA)
count += 2
# cv2.imwrite("test/frame%d.jpg" % count, image)
# images.append(imagelast)
print(count + 2)
