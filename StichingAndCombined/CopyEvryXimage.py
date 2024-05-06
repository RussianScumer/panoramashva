import os
import shutil


# Путь к исходной папке с изображениями
source_folder = r'C:\OSPanel\domains\TgBot\panoramashva\images6000'

# Путь к папке, в которую будут скопированы изображения
destination_folder = r'C:\OSPanel\domains\TgBot\panoramashva\1'

# Получаем список всех файлов в исходной папке
files = os.listdir(source_folder)

# Сортируем файлы по имени
files.sort()

# Количество изображений для копирования
images_to_copy = 10

# Перебираем файлы и копируем каждое 10-е изображение
for i, file in enumerate(files):
    if file.endswith('.jpg') or file.endswith('.png'):  # Замените на нужный формат изображений
        if (i + 1) % images_to_copy == 0:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, f'{int(i/images_to_copy + 1):03d}_{file}')
            # Проверяем, является ли файл изображением
            if os.path.isfile(source_path) and (file.endswith('.jpg') or file.endswith('.png')):
                shutil.copy(source_path, destination_path)

print('Копирование завершено.')