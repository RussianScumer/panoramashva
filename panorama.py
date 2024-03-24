import cv2
import numpy as np
from collections import deque

# Загрузка видео
cap = cv2.VideoCapture('videotest2.mp4')

# Инициализация детектора и описателя
akaze = cv2.AKAZE_create()

# Инициализация очереди для хранения изображений
frames = deque()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Изменение размера изображения для увеличения скорости обработки
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width * 0.5), int(height * 0.5)))

    # Обнаружение и описание особых точек в изображении с помощью AKAZE
    kp, desc = akaze.detectAndCompute(frame, None)

    frames.append((frame, kp, desc))

    # Чтобы не хранить все кадры, мы оставляем только последние 5 кадров
    if len(frames) > 5:
        frames.popleft()

    # Создание панорамного изображения
    if len(frames) == 5:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

        # Сравнение дескрипторов изображений
        matches = matcher.knnMatch(frames[0][2], frames[1][2], k=2)

        # Фильтрация совпадений
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Если количество хороших совпадений больше порогового значения, создаем панорамное изображение
        if len(good_matches) > 20:
            src_pts = np.float32([frames[0][1][m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([frames[1][1][m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            result = cv2.warpPerspective(frames[0][0], M, (width, height))
            #cv2.imshow("name", frames)
            #print(frames)
            result = cv2.hconcat([result, cv2.resize(frames[1][0], (50, 640, 480))])


            cv2.imwrite('Panorama.jpg', result)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

cv2.destroyAllWindows()
cap.release()