from pathlib import Path
import numpy as np
import cv2


def find_tape_coordinates(frames_folder, hsv_lower=(100, 60, 80), hsv_upper=(140, 255, 255), threshold=0.6,
                          save_masks=False, save_contours=False):
    """
	Функция находит игрек координаты изоленты нужного цвета на всех кадрах, которые находятся в рассматриваемой папке
	:param frames_folder: Путь к папке с кадрами
    :param hsv_lower: Нижняя граница HSV для маски. Функция не работает с RGB пространством, а HSV в opencv довольно специфическое, поэтому советую прочитать про это отдельно.
    :param hsv_upper: Верхняя граница HSV для маски. Эти параметры подобраны под примерный цвет изоленты. Также выделяются синие цифры и метки, но они потом отсеиваются.
    :param threshold: Порог отсеивания масок по отношению количества ненулевых пикселей к площади обёрнутого прямоугольника
    :param save_masks: Флаг, нужно ли сохранять маски. Полезно для дебага. Сохраняются в то же место, где лежат кадры
    :param save_contours: Флаг, нужно ли сохранять маски с контурами. Полезно для дебага. Сохраняются в то же место, где лежат кадры
    :return: Возвращает список кортежей (y, номер кадра)
    """
    ys = []
    for n, img_path in enumerate(sorted(Path(frames_folder).glob('*'), key=lambda x: int(
            x.stem))):  # Сортировка идёт по имени файла, который по сути номер кадра. При использовании моей старой
        # функции для порезки кадров, порядок будет правильный
        img = cv2.imread(img_path.as_posix())
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
        img = cv2.GaussianBlur(img, (5, 5), 0)  # Немного сглаживаем шумы
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Переводим картинку в HSV
        mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)  # Находим маску

        if save_masks:
            cv2.imwrite(Path(frames_folder, 'mask_' + img_path.name).as_posix(), mask)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # Находим контуры на маске
        max_cnt = max(contours, key=cv2.contourArea)  # Находим самый большой контур
        rect = cv2.minAreaRect(max_cnt)  # Находим оборачивающий прямоугольник минимальной площади
        box = cv2.boxPoints(rect)  # Находим вершины прямоугольника
        box = box.clip(0)  # Иногда вершина может быть в отрицательной области, делаем её нулём
        box = np.intp(box)

        if save_contours:
            c = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            cv2.drawContours(c, [max_cnt], 0, (255, 0, 0), 3)
            cv2.drawContours(c, [box], 0, (0, 0, 255), 3)
            cv2.imwrite(Path(frames_folder, 'contours_' + img_path.name).as_posix(), c)

        min_coords = box.min(axis=0)
        max_coords = box.max(axis=0)
        contour_crop = mask[min_coords[1]:max_coords[1], min_coords[0]:max_coords[
            0]]  # Обрезаем картинку для поиска ненулевых значений. Иначе лишние белые пиксели не дадут нормально
        # посчитать
        nonzero_pixels = np.count_nonzero(contour_crop)  # Находим количество ненулевых пикселей на части кадра
        rect_area = rect[1][0] * rect[1][1]  # Находим площадь описывающего прямоугольника
        ratio = nonzero_pixels / rect_area  # Находим отношение количества ненулевых пикселей к площади описывающего
        # прямоугольника

        if ratio < threshold:  # Таким образом отсеиваем разные синие цифры на листе и вертикальные метки, так как у
            # них очень много пустот
            print('Нет изоленты в кадре')
            continue
        else:
            ys.append((rect[0][1],
                       n))  # Добавляем координату и номер кадра. Номер нужен для случаев, когда вдруг несколько
            # кадров пропустится из-за засветов или ещё чего то и мы должны знать сколько кадров прошло.
            print('Положение изоленты', rect[0][0])
    return ys


def calculate_speed(coords, frames_discrete=1, method='mean'):
    """
    Фнукция считает среднюю либо медианную скорость. :param coords: Список кортежей из функции find_tape_coordinates
    :param frames_discrete: Сколько кадров на самом деле прошло между двумя картинками. Например, если видео резалось
    на каждый 25 кадр, то frames_discrete=25. Если каждый кадр, то frames_discrete=1 :param method: Выбор между
    средним и медианным значением. Среднее подвержено выбросам и если деталь в кадре остановится или из-за каких то
    причин плохо посчитается смещение, то это добавит ошибки. Однако если деталь всё время движется без проблем,
    средняя будет чуть точнее. :return: Возвращает скорость в пиксель на кадр
    """
    shifts = np.diff(coords, axis=0)[:, 0] / np.diff(coords, axis=0)[:,
                                             1]  # Находим смещения центра изоленты для каждого кадра. Здесь как раз
    # делим на n, чтобы учесть пропуски кадров. Если, например, изолента сместилась на 10 пикселей, но это случилось
    # за 5 кадров, то смещение равно 2.
    if method == 'median':
        speed = abs(np.median(shifts) / frames_discrete)
    else:
        speed = abs(np.mean(shifts) / frames_discrete)
    print(f'Скорость листа = {speed:.3f} пиксель/кадр')
    return speed

