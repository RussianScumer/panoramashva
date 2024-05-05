from PIL import Image

# Открываем фотографию
def CutImageOnTwoparts(panoramaDir):
    image = Image.open(panoramaDir)

# Получаем размеры фотографии
    width, height = image.size

# Вычисляем высоту первой части
    first_part_height = height - 1080

# Вычисляем координаты для разделения фотографии
    first_part_coords = (0, 0, width, first_part_height)
    second_part_coords = (0, first_part_height, width, height)

# Разделяем фотографию на две части
    first_part = image.crop(first_part_coords)
    second_part = image.crop(second_part_coords)

# Сохраняем первую часть фотографии , и далее объединяем в
    first_part.save("first_part_Panorama.jpg")

# Сохраняем вторую часть фотографии , передаем в stiching2PartWithNextImages
    second_part.save("second_part.jpg")