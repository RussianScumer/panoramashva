from PIL import Image


def crop_image_to_max_width(image_path, output_path):
    with Image.open(image_path) as img:
        # Получаем размеры изображения
        width, height = img.size

        # Обрезаем изображение
        cropped_img = img.crop((0, 631, width, height))

        # Сохраняем обрезанное изображение
        cropped_img.save(output_path)


# Пример использования функции
input_file = 'combined_panorama_vertical3 (1).jpg'
output_file = 'combined_panorama_vertical3 (1).jpg'
crop_image_to_max_width(input_file, output_file)