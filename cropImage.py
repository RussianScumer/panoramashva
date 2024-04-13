import os
from PIL import Image


def split_and_save_all_images(input_folder, output_folder):
    # Проверить, существует ли выходная папка, иначе создать ее
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Пройти по всем файлам во входной папке
    for filename in os.listdir(input_folder):
        # Проверить, что файл - изображение
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Путь к текущему изображению
            image_path = os.path.join(input_folder, filename)

            # Открыть изображение
            img = Image.open(image_path)

            # Получить размеры изображения
            width, height = img.size

            # Разделить изображение на три части по вертикали
            part_width = width // 3
            part_height = height

            # Выбрать вторую часть изображения
            box = (part_width, 0, 2 * part_width, height)
            second_part = img.crop(box)

            # Путь для сохранения второй части изображения
            output_path = os.path.join(output_folder, f"second_part_{filename}")

            # Сохранить вторую часть изображения
            second_part.save(output_path)


# Пример использования
input_folder = "1"
output_folder = "2"
split_and_save_all_images(input_folder, output_folder)