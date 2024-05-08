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

# # Перебираем все файлы в папке
# for filename in os.listdir(folder_path):
#     # Проверяем, является ли файл изображением
#     if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.gif'):
#         # Открываем изображение
#         image_path = os.path.join(folder_path, filename)
#         image = Image.open(image_path)
#
#         # Сохраняем изображение в формате PNG
#         png_filename = os.path.splitext(filename)[0] + '.png'
#         png_path = os.path.join(folder_path, png_filename)
#         image.save(png_path, 'PNG')
#
#         print(f'Изображение {filename} успешно сохранено в формате PNG: {png_filename}')
#
#         import os
#
# # Укажите путь к папке с изображениями
#         folder_path = 'путь/к/папке/с/изображениями'

        # Перебираем все файлы в папке
for filename in os.listdir(folder_path):
            # Проверяем, является ли файл изображением с расширением .jpg
            if filename.endswith('.jpg'):
                # Формируем полный путь к файлу
                file_path = os.path.join(folder_path, filename)
                # Удаляем файл
                os.remove(file_path)
                print(f'Файл {filename} успешно удален.')