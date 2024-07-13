import cv2
import numpy as np


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (_x2, _y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


def is_video_vertical(flow):
    fx, fy = flow[:, :, 0], flow[:, :, 1]
    vertical_motion = np.mean(np.abs(fy))
    horizontal_motion = np.mean(np.abs(fx))
    return vertical_motion > horizontal_motion


# Открываем видео файл
cap = cv2.VideoCapture('videos/4.mp4')

# Получаем общее количество кадров в видео
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Вычисляем индекс среднего кадра
middle_frame_index = total_frames // 2

# Устанавливаем позицию видео на средний кадр
cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)

ret, first_frame = cap.read()
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

vertical_count = 0
horizontal_count = 0

for i in range(10):
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Вычисляем оптический поток
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Визуализируем поток
    vis = draw_flow(gray, flow)

    # Показываем результат
    #cv2.imshow('Optical Flow', vis)

    # Обновляем предыдущий кадр
    prev_gray = gray

    # Определяем, идет ли видео вертикально или горизонтально
    if is_video_vertical(flow):
        vertical_count += 1
    else:
        horizontal_count += 1

    # Ждем 1 секунду перед обработкой следующего кадра
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Выводим результат
if vertical_count > horizontal_count:
    print("Видео идет вертикально")
else:
    print("Видео идет горизонтально")