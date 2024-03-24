import cv2
import numpy as np


# Функция для поиска ключевых точек и их дескрипторов с использованием AKAZE
def detectAndDescribe(image):
    # Инициализация детектора и описателя AKAZE
    descriptor = cv2.AKAZE_create()
    # Находим ключевые точки и вычисляем их описатели
    kps, descs = descriptor.detectAndCompute(image, None)
    # Преобразуем описатели в массив NumPy
    descs = descs.astype(np.float32)
    return kps, descs


# Функция для сопоставления ключевых точек между двумя изображениями
def matchKeyPoints(kpsA, kpsB, featuresA, featuresB, ratio=0.75, reprojThresh=4.0):
    # Инициализация объекта поиска соответствий
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    # Сопоставляем дескрипторы двух изображений
    rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
    matches = []

    # Фильтрация совпадений
    for m in rawMatches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            matches.append((m[0].trainIdx, m[0].queryIdx))

    # Проверка соответствий с помощью RANSAC
    if len(matches) > 4:
        # Извлекаем координаты ключевых точек для соответствующих индексов
        ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
        ptsB = np.float32([kpsB[i].pt for (i, _) in matches])
        # Используем метод RANSAC для оценки гомографии
        (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
        # Возвращаем гомографию и статус соответствий
        return (matches, H, status)
    # Возвращаем None, если совпадений недостаточно
    return None


# Загрузка видео
cap = cv2.VideoCapture('videotest.mp4')

# Инициализация переменных для хранения изображений и ключевых точек
images = []
keypoints = []

# Чтение видео и извлечение кадров
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    # Конвертация кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Добавляем оттенок серого кадра в список изображений
    images.append(gray)
    # Детекция ключевых точек и их дескрипторов с использованием AKAZE
    kps, descs = detectAndDescribe(gray)
    keypoints.append((kps, descs))

# Закрытие видеофайла
cap.release()

# Инициализация переменных для хранения соответствий и гомографий
matches = []
homographies = []

# Сопоставление ключевых точек между соседними кадрами
for i in range(len(keypoints) - 1):
    # Сопоставляем ключевые точки
    match = matchKeyPoints(keypoints[i][0], keypoints[i + 1][0], keypoints[i][1], keypoints[i + 1][1])
    if match is not None:
        matches.append(match[0])
        homographies.append(match[1])

# Определение общего размера панорамы
panorama_width = images[0].shape[1]
panorama_height = images[0].shape[0]

for i in range(1, len(images)):
    panorama_width += homographies[i - 1].shape[1]

# Создание пустого холста для панорамы
result = np.zeros((panorama_height, panorama_width), dtype=np.uint8)

# Инициализация смещения по горизонтали
offset = 0

# Объединение кадров в панораму
for i in range(len(images)):
    if i < len(homographies):  # Проверяем, что гомография существует для текущего кадра
        # Смещение и перспективное преобразование текущего кадра
        result_temp = cv2.warpPerspective(images[i], homographies[i], (panorama_width, panorama_height))
        # Объединение кадра с панорамой
        result[:, offset:offset + images[i].shape[1]] = result_temp[:, offset:offset + images[i].shape[1]]
        # Увеличение смещения
        offset += homographies[i].shape[1]

# Отображение и сохранение панорамного изображения
cv2.imshow("Panorama", result)
cv2.imwrite("panorama.jpg", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
