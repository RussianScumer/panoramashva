import os
from PIL import Image

# Укажите путь к папке с изображениями
folder_path = 'C:\OSPanel\domains\TgBot\panoramashva\images6002'
for filename in os.listdir(folder_path):
            # Проверяем, является ли файл изображением с расширением .jpg
            if filename.endswith('.jpg'):
                # Формируем полный путь к файлу
                file_path = os.path.join(folder_path, filename)
                # Удаляем файл
                os.remove(file_path)
                print(f'Файл {filename} успешно удален.')

for filename in os.listdir(folder_path):
            # Проверяем, является ли файл изображением с расширением .jpg
            if filename.endswith('.jpg'):
                # Формируем полный путь к файлу
                file_path = os.path.join(folder_path, filename)
                # Удаляем файл
                os.remove(file_path)
                print(f'Файл {filename} успешно удален.')