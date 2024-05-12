import cv2
from stitching.images import Images
import cv2
import os
from stitching import AffineStitcher
stitcher = AffineStitcher(
    nfeatures= 2000,
    min_matches=4,
    confidence_threshold=0.95,
    ransac_threshold=3.0,
    blend_type='linear',
    blend_width=32,
    crop=True,
    output_size=None
)

# Путь к папке с изображениями
image_folder = r'C:\OSPanel\domains\TgBot\panoramashva\images6002'

# Получение списка файлов изображений из папки
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))]

# Загрузка изображений
images = [cv2.imread(f) for f in image_files]

# Создание объекта Stitcher с указанными настройками
stitcher = Stitcher(**stitcher_settings)

# Склейка изображений
panorama = stitcher.stitch(images)

# Сохранение результирующей панорамы
output_file = "path/to/save/panorama.jpg"
cv2.imwrite(output_file, panorama)