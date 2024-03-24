import cv2
import numpy as np


# Функция для нахождения ключевых точек и их дескрипторов с помощью AKAZE
def detect_and_compute(image):
    akaze = cv2.AKAZE.create()
    keypoints, descriptors = akaze.detectAndCompute(image, None)
    return keypoints, descriptors


# Функция для сопоставления ключевых точек и создания панорамы
def create_panorama(images):
    # Находим ключевые точки и дескрипторы для первого изображения
    global panorama
    keypoints1, descriptors1 = detect_and_compute(images[0])

    # Создаем объект Matcher для сопоставления ключевых точек
    matcher = cv2.DescriptorMatcher.create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    panorama = images[0]
    # Проходим по остальным изображениям
    for i in range(1, len(images)):
        # Находим ключевые точки и дескрипторы для текущего изображения
        keypoints2, descriptors2 = detect_and_compute(images[i])

        # Сопоставляем ключевые точки между текущим и предыдущим изображениями
        matches = matcher.match(descriptors1, descriptors2)

        # Сортируем матчи по расстоянию
        matches = sorted(matches, key=lambda x: x.distance)

        # Выбираем только лучшие матчи
        good_matches = matches[:50]

        # Извлекаем координаты ключевых точек из матчей
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Используем метод наименьших квадратов для нахождения гомографической матрицы
        M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Применяем гомографическую трансформацию к текущему изображению
        warped_image = cv2.warpPerspective(images[i], M, (images[i].shape[1], images[i].shape[0]))

        # Обновляем панораму
        panorama = cv2.addWeighted(warped_image, 0.5, panorama, 0.5, 0)

    return panorama


# Чтение видео и создание панорамы
cap = cv2.VideoCapture('videotest2.mp4')
frames = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

panorama = create_panorama(frames)

# Отображение и сохранение панорамы
cv2.imshow('Panorama', panorama)
cv2.imwrite('panorama.jpg', panorama)
cv2.waitKey(0)
cv2.destroyAllWindows()
