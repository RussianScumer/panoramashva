from PIL import Image

def combine_images_vertically(top_image_path, bottom_image_path, output_path):
    # Открываем изображения
    top_image = Image.open(top_image_path)
    bottom_image = Image.open(bottom_image_path)

    # Определяем размеры выходного изображения
    total_width = max(top_image.width, bottom_image.width)
    total_height = top_image.height + bottom_image.height

    # Создаем новое пустое изображение с достаточным размером
    combined_image = Image.new('RGB', (total_width, total_height))

    # Размещаем первое изображение в нужной позиции
    combined_image.paste(top_image, (0, 0))

    # Сжимаем второе изображение по ширине до размеров первого изображения
    #resized_bottom_image = bottom_image.resize((top_image.width, int(bottom_image.height * top_image.width / bottom_image.width)), resample=Image.BICUBIC)

    # Размещаем второе изображение в нужной позиции
    combined_image.paste(bottom_image, (0, top_image.height))

    # Обрезаем изображение до нужного размера
    combined_image = combined_image.crop((0, 0, total_width, total_height))

    # Сохраняем объединенное изображение
    combined_image.save(output_path,"png")

# Пример использования
# top_image_path = 'first_part_Panorama.jpg'
# bottom_image_path = 'Panorama1Part.jpg'
# output_path = 'combined_panorama_vertical3.jpg'
# combine_images_vertically(top_image_path, bottom_image_path, output_path)