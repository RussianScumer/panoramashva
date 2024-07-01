import glob
import os
from PIL import Image


def combine_images_horizontally(folder_path, output_path, steps):
    # Получаем список всех файлов изображений в папке
    pattern = os.path.join(folder_path, f'{steps}_*')
    files = glob.glob(pattern)

    # Открываем все изображения
    images = [Image.open(os.path.join(folder_path, img)) for img in files]

    # Вычисляем общую ширину и максимальную высоту
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    # Создаем новое пустое изображение
    combined_image = Image.new('RGB', (total_width, max_height))

    # Размещаем изображения
    current_width = 0
    for img in images:
        combined_image.paste(img, (current_width, 0))
        current_width += img.width

    # Сохраняем объединенное изображение
    combined_image.save(output_path, "png")
    print(f"Объединенное изображение сохранено как {output_path}")



